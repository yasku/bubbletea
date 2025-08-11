¡Hola, Agustín! Por supuesto. Aquí tienes un Documento de Requisitos de Producto (PRD) completo y detallado para la construcción de tu aplicación de casa de cambio. El documento está diseñado para servir como una guía integral desde la concepción hasta el despliegue.
Documento de Requisitos de Producto (PRD): Plataforma de Gestión Cambiaria "CambioTotal"
Versión: 1.0
Fecha: 11 de Agosto de 2025
Autor: Gemini AI
Stakeholder Principal: Agustín
1. Resumen Ejecutivo
"CambioTotal" es una aplicación web interna, desarrollada en Python con el framework Streamlit, diseñada para la gestión integral de un negocio de cambio de divisas. La plataforma permitirá a los operadores y administradores realizar, registrar y supervisar operaciones de compra/venta de dólares (USD) con pesos argentinos (ARS) y, adicionalmente, operaciones con criptomonedas. La aplicación se conectará a APIs externas para obtener cotizaciones en tiempo real, garantizará la persistencia de los datos de transacciones, y ofrecerá dashboards analíticos y un panel de administración robusto para un control total del negocio. La interfaz de usuario será moderna, intuitiva y estará completamente en español.
2. Objetivos y Metas
 * Objetivos de Negocio:
   * Centralizar y digitalizar todas las operaciones de cambio.
   * Minimizar errores humanos en cálculos y registros.
   * Aumentar la eficiencia operativa y la velocidad de las transacciones.
   * Proveer visibilidad en tiempo real del estado del negocio (flujo de caja, ganancias, volumen).
   * Expandir los servicios para incluir el intercambio de criptomonedas populares.
 * Metas del Producto:
   * Desarrollar una aplicación funcional y desplegable en un plazo definido.
   * Lograr una tasa de adopción del 100% por parte de los operadores internos.
   * Mantener una latencia inferior a 2 segundos para la obtención de cotizaciones de las APIs.
   * Garantizar la integridad y seguridad de todos los registros de transacciones.
3. Perfiles de Usuario y Roles
 * Administrador:
   * Descripción: Tiene control total sobre la aplicación. Generalmente, el dueño o gerente del negocio.
   * Permisos:
     * Acceso a todas las páginas de la aplicación.
     * Realizar operaciones de cambio (Fiat y Cripto).
     * Ver todos los dashboards.
     * Gestionar usuarios (crear, editar, eliminar operadores).
     * Configurar parámetros del sistema (ej. comisiones, spreads, claves de API).
     * Ver, editar y anular cualquier transacción.
 * Operador / Cajero:
   * Descripción: Personal encargado de ejecutar las transacciones diarias con clientes.
   * Permisos:
     * Acceso a las páginas de "Operaciones Fiat" y "Operaciones Cripto".
     * Acceso a los dashboards en modo de solo lectura para ver el resumen del día/semana.
     * No tiene acceso al Panel de Administración.
     * Puede ver su propio historial de transacciones, pero no puede editarlo ni anularlo.
4. Arquitectura y Stack Tecnológico
 * Lenguaje de Programación: Python 3.10+
 * Framework Frontend/Backend: Streamlit
 * Base de Datos: SQLite para simplicidad y despliegue rápido. (Alternativa para escalar: PostgreSQL). Se usará SQLAlchemy como ORM para abstraer las interacciones con la base de datos.
 * APIs Externas:
   * Divisas Fiat (USD/ARS): DolarAPI para cotizaciones del Dólar Blue (Compra y Venta).
   * Criptomonedas: CoinGecko API por su fiabilidad, amplio listado de monedas y un plan gratuito generoso.
 * Librerías Clave de Python:
   * streamlit: Core del framework.
   * streamlit-authenticator: Para un sistema de login seguro y gestión de roles.
   * requests: Para realizar las llamadas a las APIs externas.
   * pandas: Para la manipulación de datos y la creación de los dashboards.
   * plotly: Para gráficos interactivos y visualizaciones avanzadas.
   * sqlalchemy: Para la interacción con la base de datos.
   * python-dotenv: Para gestionar variables de entorno (claves de API, secretos).
5. Estructura de la Aplicación (Multipage)
La aplicación se organizará en un formato multipágina nativo de Streamlit, con los siguientes archivos en la carpeta pages/:
 * 01_🏠_Operaciones_Fiat.py: Página principal para operaciones con USD/ARS.
 * 02_📊_Dashboard_Fiat.py: Dashboard con métricas y análisis de las operaciones Fiat.
 * 03_🪙_Operaciones_Cripto.py: Página para operaciones con criptomonedas.
 * 04_📈_Dashboard_Cripto.py: Dashboard con métricas y análisis de las operaciones Cripto.
 * 05_⚙️_Panel_de_Administracion.py: Página restringida para administradores.
La página de inicio (app.py) será la pantalla de Login.
6. Requisitos Funcionales Detallados
6.1. Sistema de Autenticación
 * RF-1.1: La aplicación debe requerir que el usuario inicie sesión antes de acceder a cualquier contenido.
 * RF-1.2: Se utilizará streamlit-authenticator para hashear y almacenar contraseñas de forma segura en un archivo de configuración (config.yaml).
 * RF-1.3: La barra lateral de navegación mostrará las páginas permitidas según el rol del usuario (Administrador u Operador) después de iniciar sesión.
6.2. Página de Operaciones Fiat (Operaciones_Fiat.py)
 * RF-2.1: La página mostrará las cotizaciones de Dólar Blue (Compra y Venta) obtenidas en tiempo real de DolarAPI. La cotización se refrescará automáticamente cada 5 minutos o con un botón manual.
 * RF-2.2: Habrá dos formularios claros: "Vender USD" (El cliente vende USD, la casa de cambio compra) y "Comprar USD" (El cliente compra USD, la casa de cambio vende).
 * RF-2.3 (Formulario Vender USD):
   * Input: "Cantidad de USD a recibir".
   * Display (solo lectura): "Cotización de Compra", "Comisión (%)", "Total a pagar en ARS".
   * El cálculo será: Total ARS = (Cantidad USD * Cotización Compra) * (1 - Comisión Compra %).
 * RF-2.4 (Formulario Comprar USD):
   * Input: "Cantidad de USD a entregar".
   * Display (solo lectura): "Cotización de Venta", "Spread (%)", "Total a cobrar en ARS".
   * El cálculo será: Total ARS = (Cantidad USD * Cotización Venta) * (1 + Spread Venta %).
 * RF-2.5: Un botón "Registrar Transacción" que, al ser presionado, guardará los detalles en la tabla transactions_fiat de la base de datos, incluyendo: id, timestamp, tipo_operacion (compra/venta), monto_usd, monto_ars, cotizacion_aplicada, comision_spread_aplicado, id_operador.
 * RF-2.6: Mostrará una tabla con las últimas 10 transacciones realizadas por el operador logueado.
6.3. Página de Operaciones Cripto (Operaciones_Cripto.py)
 * RF-3.1: Un selector permitirá elegir la criptomoneda a operar (ej. BTC, ETH, USDT, USDC). La lista se obtendrá de la API de CoinGecko.
 * RF-3.2: Se mostrará el precio en tiempo real de la criptomoneda seleccionada contra USD, obtenido de CoinGecko.
 * RF-3.3: Formularios análogos a la sección Fiat para "Comprar Cripto" y "Vender Cripto" con pesos (ARS).
   * El cálculo considerará el precio de la cripto en USD y una cotización de "dólar cripto" configurable por el administrador.
   * Ejemplo Cálculo Compra: Total ARS = (Cantidad Cripto * Precio Cripto en USD * Cotización Dólar Cripto) * (1 + Comisión Cripto %).
 * RF-3.4: El registro de la transacción se guardará en la tabla transactions_crypto con detalles similares a la Fiat, añadiendo el nombre_cripto.
6.4. Dashboards (Fiat y Cripto)
 * RF-4.1: KPIs Principales (Métricas Clave): Usando st.metric, mostrará:
   * Volumen Total Transaccionado (USD y ARS).
   * Ganancia Bruta (calculada por comisiones y spreads).
   * Número Total de Operaciones.
   * Balance Actual de Caja (configurable por el Admin).
 * RF-4.2: Gráficos Interactivos (Plotly):
   * Gráfico de barras del volumen diario/semanal/mensual.
   * Gráfico de torta mostrando la proporción de operaciones (Compra vs. Venta).
   * Tabla de datos filtrable por fecha y tipo de operación.
 * RF-4.3: El Dashboard Fiat solo usará datos de la tabla transactions_fiat, y el Cripto de transactions_crypto.
6.5. Panel de Administración (Panel_de_Administracion.py)
 * RF-5.1 (Gestión de Usuarios):
   * CRUD completo (Crear, Leer, Actualizar, Eliminar) para usuarios con rol "Operador".
   * El admin podrá resetear contraseñas.
 * RF-5.2 (Configuración del Sistema):
   * Inputs para establecer los porcentajes de comisión (compra Fiat), spread (venta Fiat) y comisiones para operaciones cripto.
   * Input para definir la cotización del "Dólar Cripto" a usar en los cálculos.
   * Campo para gestionar las claves de API (aunque se recomienda usar variables de entorno).
 * RF-5.3 (Gestión de Transacciones):
   * Visualizador de TODAS las transacciones (Fiat y Cripto) con filtros avanzados.
   * El administrador tendrá botones para "Anular" o "Editar" una transacción (con registro de auditoría).
7. Requisitos No Funcionales
 * RFN-1 (Rendimiento): La carga de cualquier página no debe superar los 3 segundos. Las llamadas a API deben tener un timeout de 5 segundos.
 * RFN-2 (Usabilidad): La interfaz debe ser intuitiva, limpia y requerir un mínimo de clics para completar una operación. Todo el texto de la UI debe estar en español.
 * RFN-3 (Seguridad): Las contraseñas deben ser hasheadas. El acceso a las páginas debe estar estrictamente controlado por roles. Las claves de API y secretos de la app no deben estar hardcodeadas en el código.
 * RFN-4 (Mantenibilidad): El código debe estar bien comentado, seguir los estándares de PEP8 y estar estructurado en módulos lógicos (ej. db_utils.py, api_calls.py).
8. Diseño de UI/UX
 * Layout: st.set_page_config(layout="wide") para aprovechar el espacio.
 * Tema: Se definirá un tema personalizado de Streamlit (config.toml) con una paleta de colores corporativa (ej. tonos de azul, gris y blanco).
 * Componentes:
   * Uso extensivo de st.columns para organizar el contenido lado a lado.
   * st.metric para mostrar KPIs de forma destacada.
   * st.dataframe o st.data_editor para mostrar tablas de datos de forma limpia.
   * st.expander para ocultar secciones menos importantes y mantener la interfaz limpia.
   * Formularios claros con st.form para evitar que la página se recargue con cada cambio en un widget.
   * Iconos de Bootstrap o Font Awesome para mejorar la estética de los botones y la barra lateral.
9. Plan de Implementación (Tareas por Fases)
 * Fase 1: Core y Setup (1 semana)
   * [ ] Configurar el entorno de desarrollo (venv, requirements.txt).
   * [ ] Estructurar el proyecto (carpetas, archivos .py).
   * [ ] Implementar el sistema de login con streamlit-authenticator.
   * [ ] Diseñar el modelo de datos y crear los scripts de inicialización de la base de datos (SQLite/SQLAlchemy).
 * Fase 2: Módulo Fiat (2 semanas)
   * [ ] Integrar la API de DolarAPI.
   * [ ] Construir la UI de la página Operaciones_Fiat.py.
   * [ ] Implementar la lógica de cálculo y registro de transacciones Fiat.
   * [ ] Construir el Dashboard_Fiat.py con KPIs y gráficos básicos.
 * Fase 3: Panel de Administración y Módulo Cripto (2 semanas)
   * [ ] Construir la UI del Panel_de_Administracion.py.
   * [ ] Implementar la lógica de gestión de usuarios y configuración del sistema.
   * [ ] Integrar la API de CoinGecko.
   * [ ] Construir la página Operaciones_Cripto.py y el Dashboard_Cripto.py.
 * Fase 4: Pruebas, Refinamiento y Documentación (1 semana)
   * [ ] Realizar pruebas unitarias y de integración.
   * [ ] Realizar Pruebas de Aceptación de Usuario (UAT) con un operador y administrador.
   * [ ] Pulir la UI/UX basándose en el feedback.
   * [ ] Redactar la documentación final (README, Guía de Usuario).
10. Estrategia de Pruebas
 * Pruebas Unitarias: Usando pytest para probar funciones de lógica pura (ej. cálculos de comisiones, funciones de base de datos).
 * Pruebas de Integración: Scripts para verificar que las llamadas a API funcionan y que los datos se guardan correctamente en la base de datos.
 * Pruebas de UI (Manuales): Navegar por toda la aplicación, probando cada botón, formulario y filtro para asegurar que la interfaz se comporta como se espera.
 * Pruebas de Aceptación de Usuario (UAT): El stakeholder principal (Agustín) y/o un futuro operador validarán que la aplicación cumple con los requisitos del negocio en un entorno de pre-producción.
11. Configuración del Entorno y Despliegue
11.1 Configuración del Entorno Local
Se creará un archivo requirements.txt con todas las dependencias.
# requirements.txt
streamlit
streamlit-authenticator
requests
pandas
plotly
SQLAlchemy
python-dotenv

Se utilizará un archivo .env para almacenar las variables de entorno sensibles:
# .env
COINGECKO_API_KEY="tu_clave_de_api_si_es_necesaria"
APP_SECRET_KEY="una_clave_secreta_muy_larga_y_aleatoria"

11.2 Despliegue
 * Opción 1 (Recomendada para empezar): Streamlit Community Cloud. Es gratuito, se integra perfectamente con GitHub y es fácil de configurar.
 * Opción 2 (Más robusta): Dockerizar la aplicación y desplegarla en un servicio como Google Cloud Run, AWS Fargate o un VPS (DigitalOcean, Vultr). Esto proporciona más control y escalabilidad.
12. Documentación Requerida
 * README.md:
   * Descripción general del proyecto.
   * Stack tecnológico.
   * Instrucciones detalladas para configurar el entorno de desarrollo local (git clone, python -m venv venv, pip install, configurar .env).
   * Instrucciones para ejecutar la aplicación (streamlit run app.py).
 * Guía de Usuario (GUIA_DE_USUARIO.pdf):
   * Documento en español.
   * Sección para Operadores: Cómo iniciar sesión, cómo realizar una operación Fiat y Cripto, cómo leer el dashboard.
   * Sección para Administradores: Incluye todo lo anterior más cómo gestionar usuarios, configurar comisiones y utilizar las funciones avanzadas del panel de administración.
Apéndice A: Documento Jules para Configuración de Entorno en Google Cloud AI Platform Notebooks
Este es un bloque de código que puedes ejecutar en una celda de un notebook de Google Cloud AI Platform (anteriormente conocido como Jules/Datalab) para configurar el entorno.
# ==============================================================================
# JULES/GOOGLE CLOUD AI NOTEBOOK SETUP - CAMBIOTOTAL APP ENVIRONMENT
# ==============================================================================
# Autor: Gemini AI
# Fecha: 2025-08-11
# Descripción: Este script instala todas las dependencias necesarias y crea
# la estructura de directorios para el proyecto CambioTotal en este entorno de notebook.
# ==============================================================================

import os
import subprocess
import sys

# --- 1. Instalación de Dependencias ---
# Lista de paquetes de Python a instalar.
packages = [
    "streamlit",
    "streamlit-authenticator",
    "requests",
    "pandas",
    "plotly",
    "SQLAlchemy",
    "python-dotenv"
]

def install(package_list):
    """Instala una lista de paquetes usando pip."""
    for package in package_list:
        print(f"Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {package}: {e}")

print("--- Iniciando la instalación de dependencias ---")
install(packages)
print("\n--- Todas las dependencias han sido procesadas. ---")


# --- 2. Creación de la Estructura de Directorios del Proyecto ---
print("\n--- Creando la estructura de directorios del proyecto ---")
project_name = "cambiototal_app"
base_path = f"/home/jupyter/{project_name}" # Ruta común en notebooks de AI Platform

directories_to_create = [
    base_path,
    os.path.join(base_path, "pages"),
    os.path.join(base_path, "data"), # Para la base de datos SQLite y otros archivos
    os.path.join(base_path, "utils")  # Para módulos de utilidades
]

for directory in directories_to_create:
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Directorio creado/verificado: {directory}")
    except OSError as e:
        print(f"❌ Error al crear el directorio {directory}: {e}")


# --- 3. Creación de Archivos Esenciales (Stubs) ---
print("\n--- Creando archivos de código iniciales ---")

files_to_create = {
    os.path.join(base_path, ".env"): '# Agrega aquí tus variables de entorno\nAPP_SECRET_KEY="CAMBIA_ESTA_CLAVE_SECRETA"\n',
    os.path.join(base_path, "requirements.txt"): "\n".join(packages),
    os.path.join(base_path, "app.py"): '# Archivo principal de la app (Login)\nimport streamlit as st\n\nst.set_page_config(page_title="Login - CambioTotal", layout="centered")\n\nst.title("Bienvenido a CambioTotal")\nst.write("Por favor, inicie sesión para continuar.")\n# Aquí irá la lógica de streamlit-authenticator',
    os.path.join(base_path, "pages", "01_🏠_Operaciones_Fiat.py"): '# Página de Operaciones Fiat\nimport streamlit as st\n\nst.title("🏠 Operaciones Fiat (USD ↔️ ARS)")',
    os.path.join(base_path, "pages", "05_⚙️_Panel_de_Administracion.py"): '# Página de Administración\nimport streamlit as st\n\nst.title("⚙️ Panel de Administración")\nst.warning("Acceso restringido solo para administradores.")'
}

for file_path, content in files_to_create.items():
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Archivo creado: {file_path}")
    else:
        print(f"🔵 El archivo ya existe, no se sobrescribe: {file_path}")

print("\n\n🎉 ¡Entorno configurado! 🎉")
print(f"El proyecto se encuentra en: {base_path}")
print("Próximos pasos recomendados:")
print("1. Edita el archivo .env con tus claves secretas.")
print(f"2. Navega al directorio del proyecto: `cd {base_path}`")
print("3. Ejecuta la aplicación con: `streamlit run app.py`")


