import streamlit as st
import time

# 1. Configuración de página (Pantalla completa simulada)
st.set_page_config(page_title="Simulador Central Nuclear", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Mágico para darle aspecto de Panel de Control Nuclear Real
st.markdown("""
<style>
    /* Fondo oscuro y tipografía industrial */
    .stApp {
        background-color: #0d1117;
        color: #39ff14;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Estilo del texto general */
    h1, h2, h3, p, label {
        color: #39ff14 !important;
    }
    /* El número del temporizador en rojo y brillante */
    [data-testid="stMetricValue"] {
        color: #ff003c !important;
        font-size: 4rem !important;
        text-shadow: 0px 0px 15px #ff003c;
    }
    /* Cajas del panel */
    .panel-caja {
        border: 2px solid #333;
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        box-shadow: inset 0 0 10px #000;
    }
    /* Barras de progreso en verde */
    .stProgress > div > div > div {
        background-color: #39ff14;
    }
    /* Separadores */
    hr {
        border-color: #39ff14;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# 3. Inicializar variables del sistema
if 'inicio' not in st.session_state:
    st.session_state.inicio = time.time()
    st.session_state.turbina = "encendida"
    st.session_state.ventilacion = "cerrada"
    st.session_state.agua = "normal" # Puede ser 'normal', 'evacuada' o 'ingresada'
    st.session_state.reactor = "encendido"
    st.session_state.alerta = ""
    st.session_state.exito = False
    st.session_state.game_over = False

# 4. Cálculo del tiempo en tiempo real
transcurrido = time.time() - st.session_state.inicio
tiempo_restante = max(0, int(30 - transcurrido))

if tiempo_restante == 0 and not st.session_state.exito:
    st.session_state.game_over = True

# 5. Interfaz Gráfica
st.markdown("<h1 style='text-align: center;'>☢️ SISTEMA DE CONTENCIÓN DEL NÚCLEO ☢️</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Contenedor superior para el tiempo
col_vacia, col_reloj, col_vacia2 = st.columns([1, 2, 1])
with col_reloj:
    if st.session_state.game_over:
        st.metric(label="TIEMPO RESTANTE", value="00:00")
    elif st.session_state.exito:
        st.metric(label="TIEMPO RESTANTE", value="SEGURO")
    else:
        st.metric(label="TIEMPO RESTANTE", value=f"00:{str(tiempo_restante).zfill(2)}")

# Columnas principales (Barras a la izquierda, Botones a la derecha)
col_estado, col_panel = st.columns([1, 1])

with col_estado:
    st.markdown("<div class='panel-caja'>", unsafe_allow_html=True)
    st.subheader("📊 ESTADO")
    
    # Lógica de la Energía
    energia = 100 if st.session_state.reactor == "encendido" else 0
    st.write(f"⚡ Energía: {energia} MWh")
    st.progress(energia / 100)

    # Lógica de la Temperatura
    temp = 480
    if st.session_state.agua == "ingresada":
        temp = 150
    st.write(f"🌡️ Temperatura: {temp}°C")
    st.progress(min(temp/500, 1.0))
    if temp > 400:
        st.markdown("<p style='color: #ff003c;'>⚠️ CRÍTICO: TEMPERATURA SUPERA LOS 400°C</p>", unsafe_allow_html=True)

    # Lógica del Agua
    nivel_agua = 50
    if st.session_state.agua == "evacuada": nivel_agua = 0
    elif st.session_state.agua == "ingresada": nivel_agua = 100
    st.write(f"💧 Nivel de agua: {nivel_agua}%")
    st.progress(nivel_agua / 100)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_panel:
    st.markdown("<div class='panel-caja'>", unsafe_allow_html=True)
    st.subheader("🎛️ PANEL DE CONTROL")
    
    # Mostrar alertas de error si el usuario presiona en mal orden
    if st.session_state.alerta:
        st.error(st.session_state.alerta)

    # 1. Botones de Turbina
    st.write("**1. Control de Turbinas**")
    c1, c2 = st.columns(2)
    if c1.button("Encender turbina", use_container_width=True):
        st.session_state.turbina = "encendida"
    if c2.button("Detener turbina", use_container_width=True):
        st.session_state.turbina = "detenida"
        st.session_state.alerta = "" # Limpiar error

    # 2. Botones de Ventilación
    st.write("**2. Sistema de Ventilación**")
    c3, c4 = st.columns(2)
    if c3.button("Abrir ventilación", use_container_width=True):
        if st.session_state.turbina == "detenida":
            st.session_state.ventilacion = "abierta"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Detener turbina' primero."
    if c4.button("Cerrar ventilación", use_container_width=True):
        st.session_state.ventilacion = "cerrada"

    # 3. Botones de Agua
    st.write("**3. Refrigeración por Agua**")
    c5, c6 = st.columns(2)
    if c5.button("Evacuar agua", use_container_width=True):
        if st.session_state.ventilacion == "abierta":
            st.session_state.agua = "evacuada"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Abrir ventilación' primero."
            
    if c6.button("Ingresar agua", use_container_width=True):
        if st.session_state.agua == "evacuada":
            st.session_state.agua = "ingresada"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Evacuar agua' caliente primero."

    # 4. Botón de Reactor
    st.write("**4. Núcleo del Reactor**")
    if st.button("Apagar reactor", use_container_width=True):
        if st.session_state.agua == "ingresada":
            st.session_state.reactor = "apagado"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Ingresar agua' fría primero."

    st.markdown("</div>", unsafe_allow_html=True)

# 6. Botón Final de Emergencia
st.markdown("<br>", unsafe_allow_html=True)
listo = (st.session_state.turbina == "detenida" and 
         st.session_state.ventilacion == "abierta" and 
         st.session_state.agua == "ingresada" and 
         st.session_state.reactor == "apagado")

if not listo:
    st.warning("🔒 BOTÓN DE EMERGENCIA BLOQUEADO - COMPLETE LOS PASOS 1 AL 4")
    st.button("🔴 PRESIONAR BOTÓN DE EMERGENCIA", disabled=True, use_container_width=True)
else:
    if st.button("🔴 PRESIONAR BOTÓN DE EMERGENCIA", type="primary", use_container_width=True):
        st.session_state.exito = True

# 7. Estados de Fin de Juego
if st.session_state.game_over:
    st.error("💥 EXPLOSIÓN INMINENTE. PROTOCOLO FALLIDO. LOS ZOMBIES HAN SIDO MUTADOS.")
    if st.button("Reiniciar Sistema"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

if st.session_state.exito:
    st.success("✅ PROTOCOLO COMPLETADO. EL SISTEMA SE HA DETENIDO CORRECTAMENTE. ZONA SEGURA.")
    if st.button("Volver a simular"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# 8. EL MOTOR DEL TEMPORIZADOR EN TIEMPO REAL
# Esto hace que Streamlit recargue la pantalla automáticamente cada 0.5 segundos
if not st.session_state.exito and not st.session_state.game_over:
    time.sleep(0.5)
    st.rerun()
