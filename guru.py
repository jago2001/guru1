import streamlit as st
from google import genai
from google.genai import types

# Configuración de la interfaz
st.set_page_config(page_title="⚡ Gurú del Parley Pro", page_icon="⚽", layout="wide")

st.title("⚽ El Gurú del Parley - Central de Pronósticos")
st.write("Selecciona la pestaña según el tipo de jugada que busques. La IA escaneará internet en tiempo real.")

# Inicializar cliente con tu API Key
client = genai.Client()

# Barra lateral común para el nivel de riesgo
st.sidebar.header("⚙️ Configuración Global")
riesgo = st.sidebar.select_slider(
    "Nivel de riesgo preferido:",
    options=["Conservador (Seguro)", "Moderado (Equilibrado)", "Arriesgado (Alta ganancia)"]
)

# --- CREACIÓN DE LAS PESTAÑAS ---
tab_en_vivo, tab_hoy_manana, tab_largo_plazo = st.tabs([
    "🔴 Partidos EN VIVO", 
    "📅 Hoy y Mañana", 
    "🏆 A Largo Plazo"
])

# ==========================================
# 1. PESTAÑA: EN VIVO
# ==========================================
with tab_en_vivo:
    st.subheader("📺 Análisis de Partidos en Desarrollo")
    st.write("Ideal para apuestas *Live*. La IA buscará qué partidos importantes se están jugando en este mismo instante, cómo van y dónde hay valor para meter un logro rápido.")
    
    if st.button("🚀 Buscar Oportunidades En Vivo"):
        with st.spinner("Escaneando marcadores en vivo y estadísticas de los partidos actuales..."):
            prompt = f"""
            Actúa como un experto en apuestas en vivo (Live betting). 
            Busca en internet qué partidos de fútbol importantes se están jugando HOY en este mismo momento en vivo.
            Revisa los marcadores actuales, el minuto de juego si es posible, y recomiéndame de 1 a 3 jugadas en vivo según este nivel de riesgo: {riesgo}.
            Ejemplos de logros en vivo: 'Próximo equipo en anotar', 'Más de X goles en lo que queda', 'Hándicap actual'. Enfoque muy rápido y táctico.
            """
            try:
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash', contents=prompt,
                    config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
                )
                st.markdown("### 📋 Alertas de Valor en Vivo")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al buscar partidos en vivo: {e}")

# ==========================================
# 2. PESTAÑA: HOY Y MAÑANA
# ==========================================
with tab_hoy_manana:
    st.subheader("📅 Parley para la Jornada (Próximas 24-48 horas)")
    st.write("El clásico generador de parleys. Elige cuántos partidos quieres combinar para armar tu ticket de la fecha.")
    
    num_partidos = st.slider("¿Cuántos partidos quieres en el parley?", min_value=2, max_value=6, value=3, key="num_hm")
    
    if st.button("🔥 Armar Parley Hoy/Mañana"):
        with st.spinner("Analizando la cartelera de hoy y mañana..."):
            prompt = f"""
            Actúa como un tipster profesional. Busca en internet los partidos de fútbol más relevantes que se jueguen hoy o mañana.
            Arma un parley de exactamente {num_partidos} partidos basándote en estadísticas de actualidad, bajas y rachas.
            Nivel de riesgo exigido: {riesgo}.
            Estructura la respuesta con: 1. Resumen del Ticket, 2. Análisis detallado con datos reales de internet de por qué elegiste cada logro, 3. Cuota total estimada.
            """
            try:
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash', contents=prompt,
                    config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
                )
                st.markdown("### 📋 Tu Ticket Sugerido")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al armar el parley: {e}")

# ==========================================
# 3. PESTAÑA: LARGO PLAZO
# ==========================================
with tab_largo_plazo:
    st.subheader("🏆 Apuestas Futuras y Grandes Torneos")
    st.write("Para dejar el dinero corriendo a mediano/largo plazo. Pronósticos sobre quién ganará una liga, quién pasará de ronda en Champions, o campeones de copas.")
    
    torneo = st.text_input("¿Qué torneo o mercado te interesa?", placeholder="Ej: Ganador de la Champions League, Quién desciende en Premier, Mundial...")
    
    if st.button("🧠 Generar Pronóstico a Largo Plazo"):
        if not torneo:
            st.warning("Escribe el nombre de un torneo o mercado para que el Gurú pueda investigar.")
        else:
            with st.spinner(f"Analizando tendencias de largo plazo para: {torneo}..."):
                prompt = f"""
                Actúa como un analista deportivo experto en apuestas a largo plazo (Outrights / Future bets).
                Quiero que investigues en internet la situación actual del mercado: '{torneo}'.
                Dame un análisis profundo de:
                1. Quién es el favorito lógico según las cuotas actuales y los datos.
                2. El 'Underdog' o caballo negro (la jugada con cuota alta que tiene valor real de ocurrir).
                3. Una recomendación final de apuesta a largo plazo ajustada a un riesgo: {riesgo}.
                """
                try:
                    respuesta = client.models.generate_content(
                        model='gemini-2.5-flash', contents=prompt,
                        config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
                    )
                    st.markdown(f"### 🔮 Análisis de Futuros: {torneo}")
                    st.write(respuesta.text)
                except Exception as e:
                    st.error(f"Error al procesar el análisis a largo plazo: {e}")
