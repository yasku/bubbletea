import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

from utils.database import SessionLocal, User

# --- Page Configuration ---
st.set_page_config(
    page_title="CambioTotal",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Database Session ---
db = SessionLocal()

# --- Authentication ---
# Load config from YAML
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create authenticator instance
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Render the login module
name, authentication_status, username = authenticator.login(fields={'Form name': 'Inicio de Sesión'})

# --- Main Application Logic ---

if authentication_status:
    # --- Successful Login ---
    st.session_state.username = username

    # Fetch user role from the database
    current_user = db.query(User).filter(User.username == username).first()
    st.session_state.role = current_user.role if current_user else "Unknown"

    # --- Sidebar Navigation ---
    with st.sidebar:
        st.title(f"Bienvenido, {name}")
        st.write(f"Rol: **{st.session_state.role.capitalize()}**")
        st.divider()

        # Define pages and their required roles
        PAGES = {
            "Operaciones Fiat": {
                "path": "pages/01_Operaciones_Fiat.py",
                "icon": "🏠",
                "roles": ["admin", "operator"]
            },
            "Dashboard Fiat": {
                "path": "pages/02_Dashboard_Fiat.py",
                "icon": "📊",
                "roles": ["admin", "operator"]
            },
            "Operaciones Cripto": {
                "path": "pages/03_Operaciones_Cripto.py",
                "icon": "🪙",
                "roles": ["admin", "operator"]
            },
            "Dashboard Cripto": {
                "path": "pages/04_Dashboard_Cripto.py",
                "icon": "📈",
                "roles": ["admin", "operator"]
            },
            "Panel de Administración": {
                "path": "pages/05_Panel_de_Administracion.py",
                "icon": "⚙️",
                "roles": ["admin"] # Only admins can see this
            }
        }

        # Dynamically create sidebar links based on role
        for page_name, page_info in PAGES.items():
            if st.session_state.role in page_info["roles"]:
                st.page_link(page_info["path"], label=page_name, icon=page_info["icon"])

        st.divider()
        authenticator.logout('Cerrar Sesión', 'sidebar')

    # --- Main Page Content after Login ---
    st.title("💸 Plataforma CambioTotal")
    st.write("Bienvenido a la plataforma de gestión cambiaria.")
    st.info("Seleccione una opción de la barra lateral para comenzar.")

elif authentication_status is False:
    # --- Invalid Credentials ---
    st.error('Usuario o contraseña incorrectos.')

elif authentication_status is None:
    # --- No Login Attempt ---
    st.warning('Por favor, ingrese su usuario y contraseña.')

# Close the database session
db.close()
