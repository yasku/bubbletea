# CambioTotal - Currency Exchange Management Platform

This repository contains the source code for "CambioTotal", a comprehensive platform for managing a currency exchange business. The project consists of two main components:

1.  **A Python Streamlit Web Application**: A feature-rich, multi-page web UI for daily operations, including fiat and crypto transactions, user management, and system configuration.
2.  **A Go TUI Management Application**: A terminal-based user interface for administering the platform, allowing a user to start/stop the web app, view logs, and monitor key business metrics.

This project was developed based on the detailed Product Requirements Document (`STREAMLITAPP.md`).

## Project Structure

-   `/cambiototal_streamlit`: Contains the complete Python Streamlit web application.
-   `/cambiototal_tui`: Contains the Go source code for the terminal management application.

## 1. Streamlit Web Application (`cambiototal_streamlit`)

### Features
-   **Multi-page Interface**: Separate pages for Fiat Operations, Fiat Dashboard, Crypto Operations, Crypto Dashboard, and an Admin Panel.
-   **Role-Based Access Control**: `admin` and `operator` roles with different permissions.
-   **Fiat & Crypto Transactions**: Real-time price fetching from public APIs (DolarAPI, CoinGecko) to register transactions.
-   **Dashboards**: KPIs and interactive charts to visualize business performance.
-   **Admin Panel**: Functionality to manage system settings (commissions, rates) and users.

### Setup and Running
1.  **Navigate to the app directory**:
    ```bash
    cd cambiototal_streamlit
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize the database** (only needs to be done once):
    ```bash
    python3 utils/database.py
    ```
4.  **Seed the database with initial users and settings** (only needs to be done once):
    *   This script will create an admin (`agustin_admin`, pass: `admin123`) and an operator (`juan_operador`, pass: `operador123`).
    ```bash
    python3 utils/seed_database.py
    ```
5.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## 2. Go TUI Management Application (`cambiototal_tui`)

### Features
-   **Process Management**: Start and stop the Streamlit web application from the terminal.
-   **Live Log Viewer**: View the live `stdout` and `stderr` from the running Streamlit process.
-   **KPI Dashboard**: View key metrics (total volume, transaction count) read directly from the application's database.
-   **View Switching**: Use the `Tab` key to switch between the Log viewer and the Dashboard.

### Setup and Running
1.  **Navigate to the TUI directory**:
    ```bash
    cd cambiototal_tui
    ```
2.  **Install Go dependencies** (if not already present):
    ```bash
    go mod tidy
    ```
3.  **Run the application**:
    ```bash
    go run .
    ```
### TUI Controls
-   `s`: Start the Streamlit application.
-   `k`: Kill the Streamlit application.
-   `tab`: Switch between Log view and Dashboard view.
-   `r`: Refresh the dashboard data manually.
-   `q`: Quit the TUI.
