package main

import (
	"bufio"
	"database/sql"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	_ "github.com/mattn/go-sqlite3"
	"github.comcom/muesli/cancelreader"
)

// --- TUI State & Model ---
type viewMode int
const (
	logView viewMode = iota
	dashboardView
)

type dashboardData struct {
	fiatVolumeARS float64
	fiatTxCount   int
}

type model struct {
	// Process management
	process      *os.Process
	processState string
	logOutput    []string
	logReader    *bufio.Reader
	cancelReader cancelreader.CancelReader

	// DB & Dashboard
	db            *sql.DB
	currentView   viewMode
	dashboard     dashboardData

	// General
	width        int
	height       int
	err          error
}

// --- Messages ---
type logMsg string
type processFinishedMsg struct{ err error }
type dashboardDataMsg dashboardData
type errMsg struct{ err error }

// --- Initial State ---
func initialModel() model {
	db, err := sql.Open("sqlite3", "../cambiototal_streamlit/cambiototal.db?_busy_timeout=5000")
	if err != nil {
		return model{err: err}
	}

	return model{
		processState: "stopped",
		logOutput:    make([]string, 0, 100),
		db:           db,
		currentView:  logView,
	}
}

func (m model) Init() tea.Cmd {
	return tea.Batch(
		queryDashboardData(m.db),
		tea.Tick(time.Second*10, func(t time.Time) tea.Msg { // Auto-refresh dashboard
			if m.currentView == dashboardView {
				return queryDashboardData(m.db)()
			}
			return nil
		}),
	)
}

// --- DB Queries ---
func queryDashboardData(db *sql.DB) tea.Cmd {
	return func() tea.Msg {
		var totalARS float64
		var count int
		row := db.QueryRow("SELECT COALESCE(SUM(amount_ars), 0), COUNT(id) FROM transactions_fiat")
		if err := row.Scan(&totalARS, &count); err != nil {
			return errMsg{err}
		}
		return dashboardDataMsg{fiatVolumeARS: totalARS, fiatTxCount: count}
	}
}

// --- Update Logic ---
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if m.err != nil {
		if msg, ok := msg.(tea.KeyMsg); ok && msg.String() == "q" { return m, tea.Quit }
		return m, nil
	}

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			if m.process != nil { m.process.Kill() }
			if m.cancelReader != nil { m.cancelReader.Cancel() }
			return m, tea.Quit
		case "s":
			if m.processState == "running" { return m, nil }
			m.logOutput = []string{"Starting Streamlit app..."}
			m.processState = "running"
			cmd := exec.Command("streamlit", "run", "../cambiototal_streamlit/app.py")
			stdout, _ := cmd.StdoutPipe()
			stderr, _ := cmd.StderrPipe()
			if err := cmd.Start(); err != nil {
				m.err = err; return m, nil
			}
			m.process = cmd.Process
			m.cancelReader, _ = cancelreader.NewReader(io.MultiReader(stdout, stderr))
			m.logReader = bufio.NewReader(m.cancelReader)
			return m, tea.Batch(waitForOutput(m.logReader), func() tea.Msg { return processFinishedMsg{cmd.Wait()} })
		case "k":
			if m.process != nil { m.process.Kill() }
			return m, nil
		case "tab":
			m.currentView = (m.currentView + 1) % 2
		case "r":
			if m.currentView == dashboardView { return m, queryDashboardData(m.db) }
		}
	case processFinishedMsg:
		m.processState = "stopped"; m.process = nil
		if m.cancelReader != nil { m.cancelReader.Cancel() }
		m.logOutput = append(m.logOutput, fmt.Sprintf("Process finished. Error: %v", msg.err))
	case logMsg:
		m.logOutput = append(m.logOutput, string(msg))
		if len(m.logOutput) > 200 { m.logOutput = m.logOutput[1:] }
		return m, waitForOutput(m.logReader)
	case dashboardDataMsg:
		m.dashboard = dashboardData(msg)
	case errMsg:
		m.err = msg.err
	case tea.WindowSizeMsg:
		m.width, m.height = msg.Width, msg.Height
	}
	return m, nil
}

// --- View Logic ---
func (m model) View() string {
	if m.err != nil { return fmt.Sprintf("Critical Error: %v\n\nPress 'q' to quit.", m.err) }

	var s strings.Builder
	s.WriteString("--- CambioTotal TUI Manager ---\n")
	s.WriteString("[Tab] Switch View | [s] Start | [k] Kill | [r] Refresh Dash | [q] Quit\n\n")

	if m.currentView == logView {
		s.WriteString(m.viewLogs())
	} else {
		s.WriteString(m.viewDashboard())
	}
	return s.String()
}

func (m model) viewLogs() string {
	var s strings.Builder
	s.WriteString(fmt.Sprintf("Streamlit App Status: %s\n\n", m.processState))
	s.WriteString("--- Logs ---\n")
	numLines := m.height - 10
	if numLines < 1 { numLines = 1 }
	start := len(m.logOutput) - numLines
	if start < 0 { start = 0 }
	for _, line := range m.logOutput[start:] {
		s.WriteString(line + "\n")
	}
	return s.String()
}

func (m model) viewDashboard() string {
	var s strings.Builder
	s.WriteString("--- Dashboard (auto-refreshes every 10s) ---\n\n")
	s.WriteString("FIAT (USD/ARS) METRICS:\n")
	s.WriteString(fmt.Sprintf("  - Total Volume (ARS): $%.2f\n", m.dashboard.fiatVolumeARS))
	s.WriteString(fmt.Sprintf("  - Total Transactions: %d\n", m.dashboard.fiatTxCount))
	return s.String()
}

// --- Helper CMDs ---
func waitForOutput(reader *bufio.Reader) tea.Cmd {
	return func() tea.Msg {
		if reader == nil { return nil }
		line, err := reader.ReadString('\n')
		if err != nil { return nil }
		return logMsg(strings.TrimSpace(line))
	}
}

func main() {
	// Setup logging to a file
	f, err := tea.LogToFile("debug.log", "debug")
	if err != nil {
		fmt.Println("fatal:", err)
		os.Exit(1)
	}
	defer f.Close()

	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		log.Fatalf("Alas, there's been an error: %v", err)
	}
}
