import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os
import bcrypt
import pandas as pd
from utils.database import SessionLocal, SystemSetting, User, TransactionFiat, TransactionCrypto

# --- Authentication and Authorization Check ---
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.warning("Por favor, inicie sesión para acceder a esta página.")
    st.stop()
if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.error("Acceso denegado. Esta página es solo para administradores.")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Panel de Administración", layout="wide")
st.title("⚙️ Panel de Administración")

# --- Database Session ---
db = SessionLocal()

# --- TABS for organization ---
tab1, tab2, tab3 = st.tabs(["Configuración del Sistema", "Gestión de Usuarios", "Supervisión de Transacciones"])

with tab1:
    st.subheader("Configuración del Sistema")
    settings_list = db.query(SystemSetting).all()
    current_settings = {s.key: s.value for s in settings_list}
    with st.form("settings_form", border=True):
        new_settings = {}
        for key, value in current_settings.items():
            new_settings[key] = st.number_input(label=key.replace("_", " ").capitalize(), value=float(value), step=0.01, format="%.2f")
        if st.form_submit_button("Guardar Configuración", use_container_width=True):
            try:
                for key, new_value in new_settings.items():
                    setting_to_update = db.query(SystemSetting).filter(SystemSetting.key == key).one()
                    setting_to_update.value = str(new_value)
                db.commit()
                st.success("¡La configuración ha sido actualizada exitosamente!")
                st.rerun()
            except Exception as e:
                db.rollback()
                st.error(f"Error al actualizar la configuración: {e}")

with tab2:
    st.subheader("Gestión de Usuarios")
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)

    users = db.query(User).all()
    st.write("Usuarios Actuales en la Base de Datos:")
    st.dataframe([{"Username": u.username, "Nombre": u.name, "Rol": u.role} for u in users], use_container_width=True)

    with st.expander("Agregar Nuevo Usuario"):
        with st.form("add_user_form"):
            st.write("Crear un nuevo usuario para el sistema.")
            new_username = st.text_input("Username (sin espacios)")
            new_name = st.text_input("Nombre Completo")
            new_email = st.text_input("Email")
            new_password = st.text_input("Contraseña", type="password")
            new_role = st.selectbox("Rol", ["operator", "admin"])
            if st.form_submit_button("Agregar Usuario"):
                if not all([new_username, new_name, new_email, new_password, new_role]):
                    st.error("Todos los campos son obligatorios.")
                elif db.query(User).filter(User.username == new_username).first() or new_username in config['credentials']['usernames']:
                    st.error("El nombre de usuario ya existe.")
                else:
                    try:
                        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        db.add(User(username=new_username, name=new_name, role=new_role))
                        config['credentials']['usernames'][new_username] = {'email': new_email, 'name': new_name, 'password': hashed_pw}
                        with open(config_path, 'w', encoding='utf-8') as f:
                            yaml.dump(config, f, default_flow_style=False)
                        db.commit()
                        st.success(f"Usuario '{new_username}' agregado.")
                        st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Error: {e}")

    with st.expander("Eliminar Usuario"):
        users_to_delete = [u.username for u in users if u.username != st.session_state['username']]
        if not users_to_delete:
            st.info("No hay otros usuarios para eliminar.")
        else:
            with st.form("delete_user_form"):
                user_to_delete = st.selectbox("Seleccione usuario a eliminar", options=users_to_delete)
                if st.form_submit_button("Eliminar Usuario", type="primary"):
                    tx_count = db.query(TransactionFiat).filter(TransactionFiat.operator_username == user_to_delete).count()
                    if tx_count > 0:
                        st.error(f"No se puede eliminar '{user_to_delete}', tiene transacciones asociadas.")
                    else:
                        try:
                            db.query(User).filter(User.username == user_to_delete).delete()
                            del config['credentials']['usernames'][user_to_delete]
                            with open(config_path, 'w', encoding='utf-8') as f:
                                yaml.dump(config, f, default_flow_style=False)
                            db.commit()
                            st.success(f"Usuario '{user_to_delete}' eliminado.")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error: {e}")

with tab3:
    st.subheader("Supervisión de Todas las Transacciones")
    try:
        fiat_df = pd.read_sql(db.query(TransactionFiat).statement, db.bind)
        # crypto_df = pd.read_sql(db.query(TransactionCrypto).statement, db.bind) # Add when crypto is done

        if fiat_df.empty: # and crypto_df.empty:
            st.info("No hay transacciones registradas en el sistema.")
        else:
            st.write("Mostrando todas las transacciones Fiat del sistema.")
            st.dataframe(fiat_df, use_container_width=True)
            # Add crypto display later
    except Exception as e:
        st.error(f"Error al cargar las transacciones: {e}")

db.close()
