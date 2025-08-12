import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import SessionLocal, TransactionFiat
from sqlalchemy import func

# --- Authentication Check ---
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.warning("Por favor, inicie sesión para acceder a esta página.")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Dashboard Fiat", layout="wide")
st.title("📊 Dashboard de Operaciones Fiat")

# --- Database Session & Data Loading ---
db = SessionLocal()

try:
    # Load all fiat transactions into a pandas DataFrame
    query = db.query(TransactionFiat).statement
    df = pd.read_sql(query, db.bind)

    if df.empty:
        st.info("No hay transacciones Fiat para mostrar en el dashboard todavía.")
        st.stop()

    # --- Data Processing ---
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date

    # Calculate profit for each transaction
    # For 'compra' (we buy USD), profit is from commission
    # For 'venta' (we sell USD), profit is from spread
    df['profit_ars'] = df.apply(
        lambda row: (row['amount_usd'] * row['rate_applied']) * (row['commission_spread_applied'] / 100),
        axis=1
    )

    # --- KPIs ---
    st.subheader("Métricas Clave (Histórico)")

    total_volume_usd = df['amount_usd'].sum()
    total_volume_ars = df['amount_ars'].sum()
    total_profit_ars = df['profit_ars'].sum()
    total_transactions = len(df)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Volumen Total (USD)", f"${total_volume_usd:,.2f}")
    kpi2.metric("Volumen Total (ARS)", f"${total_volume_ars:,.2f}")
    kpi3.metric("Ganancia Bruta (ARS)", f"${total_profit_ars:,.2f}")
    kpi4.metric("Nº de Operaciones", f"{total_transactions}")

    st.divider()

    # --- Charts ---
    st.subheader("Análisis Visual")

    # Chart 1: Daily Volume
    daily_volume = df.groupby(df['timestamp'].dt.to_period('D'))['amount_ars'].sum().reset_index()
    daily_volume['timestamp'] = daily_volume['timestamp'].dt.to_timestamp()
    fig_daily_volume = px.bar(
        daily_volume,
        x='timestamp',
        y='amount_ars',
        title='Volumen Diario Transaccionado (ARS)',
        labels={'timestamp': 'Fecha', 'amount_ars': 'Volumen en ARS'}
    )

    # Chart 2: Operation Type Proportion
    op_counts = df['type'].value_counts().reset_index()
    op_counts.columns = ['type', 'count']
    fig_op_pie = px.pie(
        op_counts,
        names='type',
        values='count',
        title='Proporción de Operaciones (Compra vs. Venta)',
        labels={'type': 'Tipo de Operación', 'count': 'Cantidad'}
    )

    chart1, chart2 = st.columns(2)
    chart1.plotly_chart(fig_daily_volume, use_container_width=True)
    chart2.plotly_chart(fig_op_pie, use_container_width=True)

    st.divider()

    # --- Raw Data Table ---
    st.subheader("Historial Completo de Transacciones Fiat")

    # Format dataframe for display
    df_display = df[[
        'timestamp', 'type', 'amount_usd', 'amount_ars',
        'rate_applied', 'commission_spread_applied', 'operator_username'
    ]].copy()
    df_display.rename(columns={
        'timestamp': 'Fecha y Hora', 'type': 'Tipo', 'amount_usd': 'Monto USD',
        'amount_ars': 'Monto ARS', 'rate_applied': 'Tasa Aplicada',
        'commission_spread_applied': 'Comisión/Spread (%)', 'operator_username': 'Operador'
    }, inplace=True)

    st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"Ocurrió un error al construir el dashboard: {e}")

finally:
    db.close()
