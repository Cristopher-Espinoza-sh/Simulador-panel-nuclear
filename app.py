import streamlit as st
import time

# Configuración de la pantalla
st.set_page_config(page_title="Panel de Control Nuclear", layout="wide")

# Inicializar variables de estado del sistema (impiden que se borre la info al hacer clic)
if 'paso1' not in st.session_state: st.session_state.paso1 = False
if 'paso2' not in st.session_state: st.session_state.paso2 = False
if 'paso3' not in st.session_state: st.session_state.paso3 = False
if 'paso4' not in st.session_state: st.session_state.paso4 = False
if 'exito' not in st.session_state: st.session_state.exito = False
if 'tiempo_inicio' not in st.session_state: st.session_state.tiempo_inicio = time.time()

# Cálculo del temporizador en tiempo real (30 segundos)
tiempo_transcurrido = time.time() - st.session_state.tiempo_inicio
tiempo_restante = max(0, int(30 - tiempo_transcurrido))

# Encabezado de la interfaz
st.title("☢️ SISTEMA DE CONTROL DE CRISIS - CENTRAL NUCLEAR")
st.write("Premisa: Personal de limpieza atrapado. Detenga la reacción antes de que el tiempo se agote.")

# Verificar condición de Game Over por tiempo
if tiempo_restante == 0 and not st.session_state.exito:
    st.error("💥 ¡EL TIEMPO SE AGOTÓ! El reactor ha explotado. Las criaturas radioactivas han sido liberadas.")
    if st.button("Reiniciar Simulacro"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
else:
    # FILA SUPERIOR: Alertas y Temporizador
    col_alerta, col_tiempo = st.columns([3, 1])
    with col_alerta:
        if not st.session_state.paso3:
            st.error("⚠️ ALERTA: Temperatura crítica en el núcleo del reactor.")
        else:
            st.success("✔️ Alerta disipada. Temperatura bajo control.")
    with col_tiempo:
        st.metric(label="TIEMPO RESTANTE", value=f"00:{tiempo_restante:02d}")

    st.divider()

    # DISPOSICIÓN PRINCIPAL (Basada en tu Versión 2)
    # Columna Izquierda: Estado (Barras de progreso) | Columna Derecha: Pasos y Control
    col_izquierda, col_derecha = st.columns([1, 1])

    with col_izquierda:
        st.subheader("Estado del Reactor")
        
        # 1. Barra de Energía (Baja a 0 al apagar el reactor)
        energia_actual = 0 if st.session_state.paso4 else 120
        st.write(f"**Energía Generada:** {energia_actual} MWe")
        st.progress(energia_actual / 120)
        
        # 2. Barra de Temperatura (Baja de 420°C a 180°C al meter agua fría)
        temp_actual = 180 if st.session_state.paso3 else 420
        st.write(f"**Temperatura del Refrigerante:** {temp_actual}°C")
        st.progress(min(temp_actual / 500, 1.0))
        if temp_actual > 400:
            st.caption("🔴 Crítico: Supera el límite de seguridad de 400°C")
            
        # 3. Barra de Nivel de Agua (Sube de 15% a 85% en el paso 3)
        agua_actual = 85 if st.session_state.paso3 else 15
        st.write(f"**Nivel de Agua de Emergencia:** {agua_actual}%")
        st.progress(agua_actual / 100)

    with col_derecha:
        st.subheader("Guía de Procedimiento")
        st.info("Secuencia obligatoria: 1. Turbinas ➡️ 2. Ventilación ➡️ 3. Agua ➡️ 4. Reactor")
        
        st.subheader("Panel de Interruptores")
        
        # Paso 1: Turbinas
        if st.button("🔌 1. Detener Turbinas de Generación"):
            st.session_state.paso1 = True
            st.rerun()
        if st.session_state.paso1: st.caption("✅ Turbinas Apagadas")

        # Paso 2: Ventilar
        if st.button("💨 2. Ventilar Contenido Radioactivo"):
            if st.session_state.paso1:
                st.session_state.paso2 = True
            else:
                st.sidebar.error("❌ ERROR DE SECUENCIA: Detenga las turbinas primero.")
            st.rerun()
        if st.session_state.paso2: st.caption("✅ Gases Ventilados")

        # Paso 3: Agua
        if st.button("💧 3. Evacuar Agua Caliente / Ingresar Agua Fría"):
            if st.session_state.paso2:
                st.session_state.paso3 = True
            else:
                st.sidebar.error("❌ ERROR DE SECUENCIA: Ventile el contenido radioactivo primero.")
            st.rerun()
        if st.session_state.paso3: st.caption("✅ Flujo de Agua Estabilizado")

        # Paso 4: Reactor
        if st.button("🛑 4. Apagar Reactor"):
            if st.session_state.paso3:
                st.session_state.paso4 = True
            else:
                st.sidebar.error("❌ ERROR DE SECUENCIA: Regule el nivel de agua primero.")
            st.rerun()
        if st.session_state.paso4: st.caption("✅ Núcleo del Reactor Apagado")

    st.divider()

    # SECCIÓN INFERIOR: Botón de Emergencia Condicionado
    st.subheader("Fase Final del Protocolo")
    
    secuencia_correcta = st.session_state.paso1 and st.session_state.paso2 and st.session_state.paso3 and st.session_state.paso4

    if not secuencia_correcta:
        st.warning("🔒 BOTÓN DE EMERGENCIA BLOQUEADO: Complete los pasos 1 al 4 en el orden correcto para liberar el cierre de seguridad.")
        st.button("🚨 5. EJECUTAR DETENCIÓN DE EMERGENCIA", disabled=True)
    else:
        if st.button("🚨 5. EJECUTAR DETENCIÓN DE EMERGENCIA", type="primary"):
            st.session_state.exito = True
            st.rerun()

    # Pantalla de éxito
    if st.session_state.exito:
        st.balloons()
        st.success("🎉 ¡SISTEMA APAGADO CON ÉXITO! El protocolo se ejecutó a tiempo y la contención zombie fue un éxito total.")
        if st.button("Simular de nuevo"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
