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
    h1, h2, h3, p, label, li {
        color: #39ff14 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ff003c !important;
        font-size: 4rem !important;
        text-shadow: 0px 0px 15px #ff003c;
    }
    .panel-caja {
    background: linear-gradient(135deg, #7f8c8d, #bdc3c7);
    border: 4px ridge #95a5a6; /* Borde tipo relieve metálico */
    padding: 20px;
    border-radius: 4px;
    box-shadow: 10px 10px 20px rgba(0,0,0,0.6);
    color: #000 !important; /* Texto negro sobre metal para contrastar */
    }

    /* Ajustar el texto dentro del chasis de metal para que sea negro y legible */
    .panel-caja h2, .panel-caja h3, .panel-caja p, .panel-caja label {
    color: #111 !important;
    text-shadow: none !important;
    }
    
    .stProgress > div > div > div {
        background-color: #39ff14;
    }
    hr {
        border-color: #39ff14;
        opacity: 0.3;
    }
    /* Colores dinámicos para los indicadores de estado */
    .indicador-on { color: #39ff14; font-weight: bold; }
    .indicador-off { color: #ff003c; font-weight: bold; }
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

# 5. Interfaz Gráfica
st.markdown("<h1 style='text-align: center;'>☢️ SISTEMA DE CONTENCIÓN DEL NÚCLEO ☢️</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Contenedor del reloj central
col_vacia, col_reloj, col_vacia2 = st.columns([1, 2, 1])
with col_reloj:
    if st.session_state.game_over:
        st.metric(label="TIEMPO RESTANTE", value="00:00")
    elif st.session_state.exito:
        st.metric(label="TIEMPO RESTANTE", value="SEGURO")
    else:
        st.metric(label="TIEMPO RESTANTE", value=f"00:{str(tiempo_restante).zfill(2)}")

# Columnas de Estado y Control
col_estado, col_panel = st.columns([1, 1])

with col_estado:
    st.markdown("<div class='panel-caja'>", unsafe_allow_html=True)
    st.subheader("📊 ESTADO DEL SISTEMA")
    
    # NUEVO: Bloque visual enorme para el estado del Reactor
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

    st.markdown("<br>", unsafe_allow_html=True)

    # Lógica de la Energía
    energia = 100 if st.session_state.turbina == "encendida" and st.session_state.reactor == "encendido" else 0
    st.write(f"⚡ Energía: {energia} MWe")
    st.progress(energia / 100)

    # Lógica de la Temperatura
    temp = 480
    if st.session_state.agua == "ingresada":
        temp = 150
    st.write(f"🌡️ Temperatura del refrigerante: {temp}°C")
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
    
    # Lista de pasos a realizar
    st.subheader("📋 PASOS A REALIZAR")
    st.markdown("""
    1. Detener turbinas.
    2. Ventilar contenido radiactivo.
    3. Evacuar agua caliente e ingresar agua fría.
    4. Apagar reactor.
    """)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("🎛️ PANEL DE CONTROL")
    
    # Sistema de Alertas por errores
    if st.session_state.alerta:
        st.error(st.session_state.alerta)

    # 1. Botones de Turbina
    st.write("**1. Control de Turbinas**")
    c1, c2 = st.columns(2)
    if c1.button("Encender turbina", use_container_width=True):
        st.session_state.turbina = "encendida"
        st.session_state.alerta = ""
    if c2.button("Detener turbina", use_container_width=True):
        st.session_state.turbina = "detenida"
        st.session_state.alerta = ""

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
        st.session_state.alerta = ""

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

    # 4. Botones de Reactor
    st.write("**4. Núcleo del Reactor**")
    c7, c8 = st.columns(2)
    if c7.button("Encender reactor", use_container_width=True):
        st.session_state.reactor = "encendido"
        st.session_state.alerta = ""
    if c8.button("Apagar reactor", use_container_width=True):
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
    st.warning("🔒 BOTÓN DE EMERGENCIA BLOQUEADO - COMPLETE LOS PASOS 1 AL 4 EN ORDEN PARA DESBLOQUEAR")
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
if not st.session_state.exito and not st.session_state.game_over:
    time.sleep(0.5)
    st.rerun()

/* Transformar los botones planos en interruptores 3D */
.stButton > button {
    background: linear-gradient(to bottom, #4a4a4a, #2b2b2b) !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 5px !important;
    box-shadow: 0 5px 10px rgba(0,0,0,0.5), inset 0 2px 2px rgba(255,255,255,0.2) !important;
    color: #e0e0e0 !important;
    font-weight: bold !important;
    text-transform: uppercase;
    transition: all 0.1s ease !important;
}

/* Efecto al presionar el botón (hundimiento) */
.stButton > button:active {
    box-shadow: 0 1px 2px rgba(0,0,0,0.5), inset 0 2px 5px rgba(0,0,0,0.8) !important;
    transform: translateY(4px) !important;
}

/* Efecto de resplandor para simular pantalla CRT antigua */
h1, h2, h3, p, label {
    text-shadow: 0px 0px 4px rgba(57, 255, 20, 0.6) !important;
}

/* El temporizador debe parecer un display LED de siete segmentos */
[data-testid="stMetricValue"] {
    font-family: 'Courier New', Courier, monospace !important;
    background-color: #000;
    padding: 10px;
    border: 3px inset #333;
    border-radius: 5px;
    box-shadow: 0 0 10px #ff003c inset;
}
