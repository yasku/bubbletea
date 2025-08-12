import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import SessionLocal, TransactionCrypto, SystemSetting

# --- Authentication Check ---
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.warning("Por favor, inicie sesión para acceder a esta página.")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Dashboard Cripto", layout="wide")
st.title("📈 Dashboard de Operaciones Cripto")

# --- Database Session & Data Loading ---
db = SessionLocal()

try:
    # Load all crypto transactions into a pandas DataFrame
    query = db.query(TransactionCrypto).statement
    df = pd.read_sql(query, db.bind)

    if df.empty:
        st.info("No hay transacciones de criptomonedas para mostrar en el dashboard todavía.")
        st.stop()

    # --- Data Processing ---
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Calculate profit for each transaction
    df['profit_ars'] = df.apply(
        lambda row: (row['crypto_amount'] * row['usd_rate_applied'] * float(db.query(SystemSetting).filter_by(key='crypto_usd_rate').first().value)) * (row['commission_applied'] / 100),
        axis=1
    )

    # --- KPIs ---
    st.subheader("Métricas Clave (Histórico Cripto)")

    total_volume_ars = df['total_ars'].sum()
    total_profit_ars = df['profit_ars'].sum()
    total_transactions = len(df)
    unique_cryptos = df['crypto_name'].nunique()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Volumen Total (ARS)", f"${total_volume_ars:,.2f}")
    kpi2.metric("Ganancia Bruta (ARS)", f"${total_profit_ars:,.2f}")
    kpi3.metric("Nº de Operaciones", f"{total_transactions}")
    kpi4.metric("Criptos Distintas", f"{unique_cryptos}")

    st.divider()

    # --- Charts ---
    st.subheader("Análisis Visual Cripto")

    # Chart 1: Volume by Cryptocurrency
    volume_by_crypto = df.groupby('crypto_name')['total_ars'].sum().sort_values(ascending=False).reset_index()
    fig_volume_crypto = px.bar(
        volume_by_crypto,
        x='crypto_name',
        y='total_ars',
        title='Volumen Total (ARS) por Criptomoneda',
        labels={'crypto_name': 'Criptomoneda', 'total_ars': 'Volumen en ARS'}
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
    chart1.plotly_chart(fig_volume_crypto, use_container_width=True)
    chart2.plotly_chart(fig_op_pie, use_container_width=True)

    st.divider()

    # --- Raw Data Table ---
    st.subheader("Historial Completo de Transacciones Cripto")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Ocurrió un error al construir el dashboard: {e}")

finally:
    db.close()
