import streamlit as st
import pandas as pd
from utils.api_client import get_dolar_rates
from utils.database import SessionLocal, SystemSetting, TransactionFiat, User
import datetime

# --- Authentication Check ---
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.warning("Por favor, inicie sesión para acceder a esta página.")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Operaciones Fiat", layout="wide")
st.title("🏠 Operaciones Fiat (USD ↔️ ARS)")

# --- Database and User Info ---
db = SessionLocal()
username = st.session_state.get("username", "unknown")

# --- Fetch Data ---
dolar_rates = get_dolar_rates()
settings = {s.key: float(s.value) for s in db.query(SystemSetting).all()}
buy_commission_percent = settings.get("fiat_buy_commission_percent", 0.5)
sell_spread_percent = settings.get("fiat_sell_spread_percent", 0.5)

# --- UI ---
if not dolar_rates:
    st.error("No se pudieron obtener las cotizaciones del dólar. Por favor, intente de nuevo más tarde.")
    st.stop()

# Display current rates
st.subheader("Cotizaciones Dólar Blue en Tiempo Real")
col1, col2, col3 = st.columns(3)
col1.metric("Compra (Nosotros Pagamos)", f"${dolar_rates['buy']:.2f}", "ARS por 1 USD")
col2.metric("Venta (Nosotros Cobramos)", f"${dolar_rates['sell']:.2f}", "ARS por 1 USD")
if col3.button("Refrescar Cotizaciones"):
    st.cache_data.clear()
    st.rerun()

st.divider()

# --- Forms for Operations ---
col_buy, col_sell = st.columns(2)

# Form 1: Client is SELLING USD to us (we are BUYING)
with col_buy:
    with st.form("vender_usd_form", border=True):
        st.subheader("Registrar Venta de Cliente (Nosotros Compramos USD)")

        usd_amount_sell = st.number_input("Cantidad de USD que el cliente vende:", min_value=0.01, step=10.0, format="%.2f")

        # Calculation
        our_buy_price = dolar_rates['buy']
        total_ars_to_pay = (usd_amount_sell * our_buy_price) * (1 - buy_commission_percent / 100)

        st.info(f"Cotización Compra: **${our_buy_price:.2f}**")
        st.success(f"Total a Pagar al Cliente: **${total_ars_to_pay:,.2f} ARS**")

        submitted_sell = st.form_submit_button("Registrar Transacción", use_container_width=True)

        if submitted_sell:
            if usd_amount_sell > 0:
                new_transaction = TransactionFiat(
                    timestamp=datetime.datetime.utcnow(),
                    type="compra", # We are buying USD
                    amount_usd=usd_amount_sell,
                    amount_ars=total_ars_to_pay,
                    rate_applied=our_buy_price,
                    commission_spread_applied=buy_commission_percent,
                    operator_username=username
                )
                db.add(new_transaction)
                db.commit()
                st.success(f"Transacción de compra de {usd_amount_sell} USD registrada exitosamente.")
            else:
                st.error("Por favor, ingrese un monto válido.")

# Form 2: Client is BUYING USD from us (we are SELLING)
with col_sell:
    with st.form("comprar_usd_form", border=True):
        st.subheader("Registrar Compra de Cliente (Nosotros Vendemos USD)")

        usd_amount_buy = st.number_input("Cantidad de USD que el cliente compra:", min_value=0.01, step=10.0, format="%.2f")

        # Calculation
        our_sell_price = dolar_rates['sell']
        total_ars_to_collect = (usd_amount_buy * our_sell_price) * (1 + sell_spread_percent / 100)

        st.info(f"Cotización Venta: **${our_sell_price:.2f}**")
        st.success(f"Total a Cobrar al Cliente: **${total_ars_to_collect:,.2f} ARS**")

        submitted_buy = st.form_submit_button("Registrar Transacción", use_container_width=True)

        if submitted_buy:
            if usd_amount_buy > 0:
                new_transaction = TransactionFiat(
                    timestamp=datetime.datetime.utcnow(),
                    type="venta", # We are selling USD
                    amount_usd=usd_amount_buy,
                    amount_ars=total_ars_to_collect,
                    rate_applied=our_sell_price,
                    commission_spread_applied=sell_spread_percent,
                    operator_username=username
                )
                db.add(new_transaction)
                db.commit()
                st.success(f"Transacción de venta de {usd_amount_buy} USD registrada exitosamente.")
            else:
                st.error("Por favor, ingrese un monto válido.")

st.divider()

# --- Display latest transactions ---
st.subheader(f"Últimas 10 Transacciones Fiat de '{username}'")
try:
    recent_transactions = db.query(TransactionFiat)\
        .filter(TransactionFiat.operator_username == username)\
        .order_by(TransactionFiat.timestamp.desc())\
        .limit(10)\
        .all()

    if recent_transactions:
        # Convert to DataFrame for better display
        df = pd.DataFrame([{
            "Fecha": t.timestamp.strftime("%Y-%m-%d %H:%M"),
            "Tipo": t.type.capitalize(),
            "USD": f"${t.amount_usd:,.2f}",
            "ARS": f"${t.amount_ars:,.2f}",
            "Tasa Aplicada": f"${t.rate_applied:,.2f}"
        } for t in recent_transactions])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay transacciones registradas para este usuario todavía.")

except Exception as e:
    st.error(f"Error al cargar el historial de transacciones: {e}")

db.close()
