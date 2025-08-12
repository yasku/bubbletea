# Guía de Usuario - Plataforma CambioTotal

Este documento describe cómo utilizar la plataforma de gestión cambiaria "CambioTotal".

## 1. Acceso a la Aplicación

Para iniciar la aplicación web, su administrador de sistemas debe seguir las instrucciones del archivo `README.md`. Una vez iniciada, podrá acceder a ella a través de su navegador web.

La plataforma le pedirá un nombre de usuario y una contraseña. Las credenciales iniciales son:
-   **Administrador**:
    -   Usuario: `agustin_admin`
    -   Contraseña: `admin123`
-   **Operador**:
    -   Usuario: `juan_operador`
    -   Contraseña: `operador123`

## 2. Funcionalidades para Operadores

Como operador, tendrá acceso a las siguientes páginas desde la barra lateral izquierda:

### 2.1. Operaciones Fiat
-   Aquí puede registrar transacciones de compra y venta de Dólares (USD) a cambio de Pesos Argentinos (ARS).
-   Las cotizaciones de "Compra" y "Venta" se muestran en tiempo real.
-   Utilice los formularios para ingresar el monto en USD que el cliente desea comprar o vender. El sistema calculará automáticamente el total en ARS aplicando las comisiones correspondientes.
-   Haga clic en "Registrar Transacción" para guardar la operación.
-   Debajo de los formularios, verá una tabla con sus últimas 10 transacciones.

### 2.2. Dashboard Fiat
-   Esta página muestra un resumen de todas las operaciones con Dólares.
-   Podrá ver métricas clave (KPIs) como el volumen total transaccionado y la cantidad de operaciones.
-   Gráficos interactivos le permitirán visualizar el rendimiento diario y la proporción de compras vs. ventas.

### 2.3. Operaciones Cripto
-   Similar a la página de Operaciones Fiat, pero para criptomonedas.
-   Seleccione la criptomoneda deseada (e.g., Bitcoin, Ethereum).
-   El sistema mostrará el precio actual en USD y utilizará la tasa "Dólar Cripto" configurada por el administrador para realizar los cálculos en ARS.
-   Complete los formularios para registrar la compra o venta de criptoactivos.

### 2.4. Dashboard Cripto
-   Un resumen visual de todas las operaciones con criptomonedas, con sus propios KPIs y gráficos.

## 3. Funcionalidades para Administradores

Como administrador, tiene acceso a todas las funcionalidades de los operadores, más el **Panel de Administración**.

### 3.1. Panel de Administración
Esta página está organizada en tres pestañas:

-   **Configuración del Sistema**: Le permite ver y modificar los parámetros globales del negocio, como los porcentajes de comisión para operaciones Fiat, los spreads, y la tasa de "Dólar Cripto". Simplemente cambie los valores y haga clic en "Guardar".
-   **Gestión de Usuarios**:
    -   Vea una lista de todos los usuarios del sistema.
    -   Agregue nuevos usuarios (tanto operadores como otros administradores) proporcionando sus datos y una contraseña inicial.
    -   Elimine usuarios existentes. **Nota**: No podrá eliminar un usuario que tenga transacciones registradas.
-   **Supervisión de Transacciones**:
    -   Vea una tabla con el historial completo de **todas** las transacciones (Fiat y Cripto) realizadas por todos los operadores.

## 4. Uso de la TUI de Administración (Opcional)

Para administradores con acceso a la línea de comandos del servidor, la TUI (Terminal User Interface) ofrece una forma rápida de gestionar la aplicación.

-   **Navegue a la carpeta `cambiototal_tui` y ejecute `go run .`**
-   **Controles**:
    -   `s`: Inicia el servidor de la aplicación web de Streamlit.
    -   `k`: Detiene el servidor.
    -   `tab`: Cambia entre la vista de Logs (registros del servidor) y la vista de Dashboard (KPIs).
    -   `r`: Refresca los datos del dashboard.
    -   `q`: Cierra la TUI.
