import streamlit as st
import time

# 1. Configuración de página (Pantalla completa simulada)
st.set_page_config(page_title="Simulador Central Nuclear", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Avanzado: Esqueumorfismo (Efectos Metálicos, CRT, 3D y Textura de Fondo)
st.markdown("""
<style>
    /* Fondo exterior con textura de acero perforado industrial */
    .stApp {
        background-color: #121212;
        background-image: radial-gradient(#2a2a2a 15%, transparent 16%), radial-gradient(#2a2a2a 15%, transparent 16%);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
    }

    /* Título principal con efecto resplandor CRT */
    h1 {
        color: #39ff14 !important;
        text-shadow: 0px 0px 10px rgba(57, 255, 20, 0.7) !important;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
    }

    /* Display LED para el temporizador */
    [data-testid="stMetricValue"] {
        color: #ff003c !important;
        font-size: 4.5rem !important;
        font-family: 'Courier New', Courier, monospace !important;
        text-shadow: 0px 0px 15px #ff003c;
        background-color: #050505;
        padding: 15px 30px;
        border: 4px inset #222;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(255, 0, 60, 0.2) inset;
        display: flex;
        justify-content: center;
    }
    
    [data-testid="stMetricLabel"] {
        color: #39ff14 !important;
        font-weight: bold;
        font-size: 1.2rem !important;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Chasis Metálico para los paneles */
    .panel-caja {
        background: linear-gradient(135deg, #8e9eab, #eef2f3);
        border: 4px ridge #95a5a6;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.7), inset 0 0 20px rgba(255,255,255,0.5);
        height: 100%;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Forzar que todo el texto dentro del chasis de metal sea oscuro */
    .panel-caja p, .panel-caja strong, .panel-caja h2, .panel-caja h3, .panel-caja li, .panel-caja div {
        color: #111 !important;
        text-shadow: none !important;
    }

    /* Transformar los botones planos en interruptores industriales 3D */
    .stButton > button {
        background: linear-gradient(to bottom, #5c5c5c, #2b2b2b) !important;
        border: 2px solid #111 !important;
        border-radius: 6px !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.6), inset 0 2px 2px rgba(255,255,255,0.3) !important;
        color: #fff !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        font-family: 'Courier New', Courier, monospace;
        transition: all 0.1s ease !important;
    }

    /* Efecto de hundimiento al presionar el interruptor */
    .stButton > button:active {
        box-shadow: 0 1px 2px rgba(0,0,0,0.8), inset 0 4px 8px rgba(0,0,0,0.9) !important;
        transform: translateY(5px) !important;
    }
    
    /* Botón de Emergencia (Rojo vibrante 3D) */
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(to bottom, #e74c3c, #96281b) !important;
        box-shadow: 0 6px 15px rgba(231, 76, 60, 0.6), inset 0 2px 2px rgba(255,255,255,0.4) !important;
    }
    
    .stButton > button[data-baseweb="button"][kind="primary"]:active {
        box-shadow: 0 1px 2px rgba(0,0,0,0.8), inset 0 4px 8px rgba(0,0,0,0.9) !important;
    }

    /* Colores de las barras de progreso para que destaquen sobre el metal */
    .stProgress > div > div > div {
        background-color: #27ae60 !important;
    }

    /* Indicadores de estado visuales */
    .indicador-on { color: #1e8449 !important; font-weight: 900; background-color: rgba(39,174,96,0.2); padding: 2px 5px; border-radius: 3px; border: 1px solid #1e8449;}
    .indicador-off { color: #c0392b !important; font-weight: 900; background-color: rgba(192,57,43,0.2); padding: 2px 5px; border-radius: 3px; border: 1px solid #c0392b;}
    
    hr {
        border-color: #555;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# 3. Inicializar variables del sistema
if 'inicio' not in st.session_state:
    st.session_state.inicio = time.time()
    st.session_state.turbina = "encendida"
    st.session_state.ventilacion = "cerrada"
    st.session_state.agua = "normal" 
    st.session_state.reactor = "encendido"
    st.session_state.alerta = ""
    st.session_state.exito = False
    st.session_state.game_over = False

# 4. Cálculo del tiempo en tiempo real
transcurrido = time.time() - st.session_state.inicio
tiempo_restante = max(0, int(30 - transcurrido))

if tiempo_restante == 0 and not st.session_state.exito:
    st.session_state.game_over = True

# 5. Interfaz Gráfica Principal
st.markdown("<h1>☢️ SISTEMA DE CONTENCIÓN DEL NÚCLEO ☢️</h1>", unsafe_allow_html=True)

# Contenedor del reloj central
col_vacia, col_reloj, col_vacia2 = st.columns([1, 2, 1])
with col_reloj:
    if st.session_state.game_over:
        st.metric(label="TIEMPO RESTANTE", value="00:00")
    elif st.session_state.exito:
        st.metric(label="TIEMPO RESTANTE", value="SEGURO")
    else:
        st.metric(label="TIEMPO RESTANTE", value=f"00:{str(tiempo_restante).zfill(2)}")

st.markdown("<br>", unsafe_allow_html=True)

# Columnas de Estado y Control (El Chasis Metálico)
col_estado, col_panel = st.columns([1, 1])

with col_estado:
    st.markdown("<div class='panel-caja'>", unsafe_allow_html=True)
    st.markdown("<h3>📊 ESTADO DEL SISTEMA</h3>", unsafe_allow_html=True)
    
    # Bloque visual para el estado del Reactor
    if st.session_state.reactor == "encendido":
        st.error("☢️ NÚCLEO DEL REACTOR: EN LÍNEA (PELIGRO DE FUSIÓN)")
    else:
        st.success("✅ NÚCLEO DEL REACTOR: APAGADO (ESTABILIZADO)")
    st.markdown("<br>", unsafe_allow_html=True)

    # Indicadores visuales de Turbina, Ventilación y Reactor
    turbina_color = "indicador-on" if st.session_state.turbina == "encendida" else "indicador-off"
    turbina_texto = "EN MARCHA" if st.session_state.turbina == "encendida" else "DETENIDAS"
    st.markdown(f"🔄 **Turbinas:** <span class='{turbina_color}'>{turbina_texto}</span>", unsafe_allow_html=True)
    
    vent_color = "indicador-off" if st.session_state.ventilacion == "cerrada" else "indicador-on"
    vent_texto = "CERRADA" if st.session_state.ventilacion == "cerrada" else "ABIERTA"
    st.markdown(f"💨 **Ventilación:** <span class='{vent_color}'>{vent_texto}</span>", unsafe_allow_html=True)
    
    reactor_color = "indicador-off" if st.session_state.reactor == "encendido" else "indicador-on"
    reactor_texto = "ACTIVO" if st.session_state.reactor == "encendido" else "APAGADO"
    st.markdown(f"☢️ **Reactor:** <span class='{reactor_color}'>{reactor_texto}</span>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Lógica de la Energía
    energia = 100 if st.session_state.turbina == "encendida" and st.session_state.reactor == "encendido" else 0
    st.write(f"⚡ **Energía Generada:** {energia} MWe")
    st.progress(energia / 100)

    # Lógica de la Temperatura
    temp = 480
    if st.session_state.agua == "ingresada":
        temp = 150
    st.write(f"🌡️ **Temperatura del refrigerante:** {temp}°C")
    st.progress(min(temp/500, 1.0))
    if temp > 400:
        st.markdown("<p style='color: #c0392b; font-weight: bold;'>⚠️ CRÍTICO: TEMPERATURA SUPERA LOS 400°C</p>", unsafe_allow_html=True)

    # Lógica del Agua
    nivel_agua = 50
    if st.session_state.agua == "evacuada": nivel_agua = 0
    elif st.session_state.agua == "ingresada": nivel_agua = 100
    st.write(f"💧 **Nivel de agua de emergencia:** {nivel_agua}%")
    st.progress(nivel_agua / 100)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_panel:
    st.markdown("<div class='panel-caja'>", unsafe_allow_html=True)
    
    # Lista de pasos a realizar
    st.markdown("<h3>📋 PROCEDIMIENTO</h3>", unsafe_allow_html=True)
    st.markdown("""
    1. Detener turbinas.
    2. Ventilar contenido radiactivo.
    3. Evacuar agua caliente e ingresar agua fría.
    4. Apagar reactor.
    """)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h3>🎛️ PANEL DE INTERRUPTORES</h3>", unsafe_allow_html=True)
    
    # Sistema de Alertas por errores
    if st.session_state.alerta:
        st.error(st.session_state.alerta)

    # 1. Botones de Turbina
    st.write("**[ 1 ] CONTROL DE TURBINAS**")
    c1, c2 = st.columns(2)
    if c1.button("Encender", use_container_width=True):
        st.session_state.turbina = "encendida"
        st.session_state.alerta = ""
    if c2.button("Detener", use_container_width=True):
        st.session_state.turbina = "detenida"
        st.session_state.alerta = ""

    # 2. Botones de Ventilación
    st.write("**[ 2 ] SISTEMA DE VENTILACIÓN**")
    c3, c4 = st.columns(2)
    if c3.button("Abrir", use_container_width=True):
        if st.session_state.turbina == "detenida":
            st.session_state.ventilacion = "abierta"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Detener' las turbinas primero."
    if c4.button("Cerrar", use_container_width=True):
        st.session_state.ventilacion = "cerrada"
        st.session_state.alerta = ""

    # 3. Botones de Agua
    st.write("**[ 3 ] REFRIGERACIÓN POR AGUA**")
    c5, c6 = st.columns(2)
    if c5.button("Evacuar Agua", use_container_width=True):
        if st.session_state.ventilacion == "abierta":
            st.session_state.agua = "evacuada"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Abrir' la ventilación primero."
    if c6.button("Ingresar Fría", use_container_width=True):
        if st.session_state.agua == "evacuada":
            st.session_state.agua = "ingresada"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Evacuar Agua' caliente primero."

    # 4. Botones de Reactor
    st.write("**[ 4 ] NÚCLEO DEL REACTOR**")
    c7, c8 = st.columns(2)
    if c7.button("Activar Reactor", use_container_width=True):
        st.session_state.reactor = "encendido"
        st.session_state.alerta = ""
    if c8.button("Apagar Reactor", use_container_width=True):
        if st.session_state.agua == "ingresada":
            st.session_state.reactor = "apagado"
            st.session_state.alerta = ""
        else:
            st.session_state.alerta = "ERROR SECUENCIA: Debe 'Ingresar Fría' primero."

    st.markdown("</div>", unsafe_allow_html=True)

# 6. Botón Final de Emergencia (Aislado visualmente)
st.markdown("<br>", unsafe_allow_html=True)
listo = (st.session_state.turbina == "detenida" and 
         st.session_state.ventilacion == "abierta" and 
         st.session_state.agua == "ingresada" and 
         st.session_state.reactor == "apagado")

col_izq, col_btn, col_der = st.columns([1, 2, 1])
with col_btn:
    if not listo:
        st.warning("🔒 BOTÓN DE EMERGENCIA BLOQUEADO - COMPLETE LOS PASOS 1 AL 4 PARA DESBLOQUEAR")
        st.button("🔴 PRESIONAR BOTÓN DE EMERGENCIA", disabled=True, use_container_width=True)
    else:
        st.info("🔓 BLOQUEO DE SEGURIDAD LIBERADO")
        if st.button("🔴 PRESIONAR BOTÓN DE EMERGENCIA", type="primary", use_container_width=True):
            st.session_state.exito = True

# 7. Estados de Fin de Juego
if st.session_state.game_over:
    st.error("💥 EXPLOSIÓN INMINENTE. PROTOCOLO FALLIDO. LOS ZOMBIES HAN SIDO MUTADOS.")
    if st.button("Reiniciar Sistema"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

if st.session_state.exito:
    st.balloons()
    st.success("✅ PROTOCOLO COMPLETADO. EL SISTEMA SE HA DETENIDO CORRECTAMENTE. ZONA SEGURA.")
    if st.button("Volver a simular"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# 8. EL MOTOR DEL TEMPORIZADOR EN TIEMPO REAL
if not st.session_state.exito and not st.session_state.game_over:
    time.sleep(0.5)
    st.rerun()
