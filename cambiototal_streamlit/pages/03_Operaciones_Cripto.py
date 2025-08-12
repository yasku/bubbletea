import streamlit as st
from utils.api_client import get_crypto_prices
from utils.database import SessionLocal, SystemSetting, TransactionCrypto
import datetime

# --- Authentication Check ---
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.warning("Por favor, inicie sesión para acceder a esta página.")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Operaciones Cripto", layout="wide")
st.title("🪙 Operaciones con Criptomonedas")

# --- Database and User Info ---
db = SessionLocal()
username = st.session_state.get("username", "unknown")

# --- Configurable Data ---
# List of available cryptos (can be expanded)
AVAILABLE_CRYPTOS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Tether": "tether",
    "USDC": "usd-coin"
}
settings = {s.key: float(s.value) for s in db.query(SystemSetting).all()}
dolar_cripto_rate = settings.get("crypto_usd_rate", 1000.0)
buy_commission = settings.get("crypto_buy_commission_percent", 1.0)
sell_commission = settings.get("crypto_sell_commission_percent", 1.0)

# --- UI ---
st.info(f"Usando una cotización de **Dólar Cripto = ${dolar_cripto_rate:,.2f} ARS** (configurable por el admin).")
st.divider()

# --- Crypto Selection and Price Display ---
selected_crypto_name = st.selectbox("Seleccione una Criptomoneda", options=list(AVAILABLE_CRYPTOS.keys()))
selected_crypto_id = AVAILABLE_CRYPTOS[selected_crypto_name]

prices = get_crypto_prices([selected_crypto_id])

if not prices or selected_crypto_id not in prices:
    st.error(f"No se pudo obtener el precio de {selected_crypto_name}. Intente de nuevo.")
    st.stop()

current_price_usd = prices[selected_crypto_id]['usd']
st.metric(f"Precio Actual de {selected_crypto_name}", f"${current_price_usd:,.2f} USD")

st.divider()

# --- Forms for Operations ---
col_buy, col_sell = st.columns(2)

# Form 1: Client Buys Crypto
with col_buy:
    with st.form("buy_crypto_form", border=True):
        st.subheader(f"Cliente Compra {selected_crypto_name}")
        crypto_amount = st.number_input(f"Cantidad de {selected_crypto_name} a comprar:", min_value=0.00001, step=0.01, format="%.5f")

        # Calculation
        total_ars = (crypto_amount * current_price_usd * dolar_cripto_rate) * (1 + buy_commission / 100)

        st.success(f"Total a Cobrar al Cliente: **${total_ars:,.2f} ARS**")

        submitted_buy = st.form_submit_button("Registrar Compra", use_container_width=True)
        if submitted_buy and crypto_amount > 0:
            tx = TransactionCrypto(
                type="compra", crypto_name=selected_crypto_name, crypto_amount=crypto_amount,
                total_ars=total_ars, usd_rate_applied=current_price_usd,
                commission_applied=buy_commission, operator_username=username
            )
            db.add(tx)
            db.commit()
            st.success("Transacción de compra de cripto registrada.")

# Form 2: Client Sells Crypto
with col_sell:
    with st.form("sell_crypto_form", border=True):
        st.subheader(f"Cliente Vende {selected_crypto_name}")
        crypto_amount_sell = st.number_input(f"Cantidad de {selected_crypto_name} a vender:", min_value=0.00001, step=0.01, format="%.5f")

        # Calculation
        total_ars_sell = (crypto_amount_sell * current_price_usd * dolar_cripto_rate) * (1 - sell_commission / 100)

        st.success(f"Total a Pagar al Cliente: **${total_ars_sell:,.2f} ARS**")

        submitted_sell = st.form_submit_button("Registrar Venta", use_container_width=True)
        if submitted_sell and crypto_amount_sell > 0:
            tx = TransactionCrypto(
                type="venta", crypto_name=selected_crypto_name, crypto_amount=crypto_amount_sell,
                total_ars=total_ars_sell, usd_rate_applied=current_price_usd,
                commission_applied=sell_commission, operator_username=username
            )
            db.add(tx)
            db.commit()
            st.success("Transacción de venta de cripto registrada.")

db.close()
