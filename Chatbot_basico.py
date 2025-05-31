import streamlit as st

st.set_page_config(page_title="Chatbot MZF", layout="centered")

st.title("🎾 Chatbot MZF - Torneos de Tenis")
st.markdown("Hablá con el asistente para inscribirte, pasar resultados o consultar info.")

# Inicializamos variables de estado
if "estado" not in st.session_state:
    st.session_state.estado = "esperando_saludo"
if "jugador" not in st.session_state:
    st.session_state.jugador = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial del chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Captura de mensaje
if prompt := st.chat_input("Escribí tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    lower_prompt = prompt.lower()

    # 1. Esperando saludo
    if st.session_state.estado == "esperando_saludo":
        if any(p in lower_prompt for p in ["hola", "buenas", "qué tal"]):
            response = "¡Hola! Qué gusto saludarte 😊 ¿Cómo te llamás?"
            st.session_state.estado = "esperando_nombre"
        else:
            response = "👋 Para comenzar, saludame con un 'hola', 'buenas' o algo por el estilo."
    
    # 2. Esperando nombre
    elif st.session_state.estado == "esperando_nombre":
        st.session_state.jugador = prompt.strip()
        response = f"¡Encantado, {st.session_state.jugador}! ¿En qué puedo ayudarte?"
        st.session_state.estado = "listo"
    
    # 3. Chat normal
    elif st.session_state.estado == "listo":
        nombre_jugador = st.session_state.jugador

        if any(p in lower_prompt for p in ["gracias", "muchas gracias"]):
            response = f"¡De nada, {nombre_jugador}! Estoy para ayudarte."
        elif any(p in lower_prompt for p in ["chau", "nos vemos", "hasta luego"]):
            response = f"¡Hasta luego, {nombre_jugador}! Que tengas un gran día 🎾"
        elif "inscribirme" in lower_prompt:
            response = f"{nombre_jugador}, te anoté en el torneo. ¡Mucha suerte!"
        elif "/" in prompt or "gané" in lower_prompt:
            response = f"Perfecto, {nombre_jugador}, anoté tu resultado."
        elif "cuándo" in lower_prompt and "juego" in lower_prompt:
            response = f"{nombre_jugador}, tu partido es el sábado a las 15hs contra G. López."
        else:
            response = f"No entendí bien, {nombre_jugador}. ¿Podés reformular tu pregunta?"

    # Mostrar respuesta del bot
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
