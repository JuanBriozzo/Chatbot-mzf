import streamlit as st

st.set_page_config(page_title="Chatbot MZF", layout="centered")

st.title("🎾 Chatbot MZF - Torneos de Tenis")
st.markdown("Hablá con el asistente para inscribirte, pasar resultados o consultar info.")

if "jugador" not in st.session_state:
    st.session_state.jugador = None

if st.session_state.jugador is None:
    st.write("👋 Hola, antes de empezar necesito saber quién sos.")
    nombre = st.text_input("Escribí tu nombre y apellido:")
    if nombre:
        st.session_state.jugador = nombre
        st.success(f"¡Gracias, {nombre}! Ahora sí podemos empezar.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribí tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    nombre_jugador = st.session_state.jugador

    if "inscribirme" in prompt.lower():
        response = f"{nombre_jugador}, te anoté en el torneo. ¡Mucha suerte!"
    elif "/" in prompt or "gané" in prompt.lower():
        response = f"Perfecto, {nombre_jugador}, anoté tu resultado."
    elif "cuándo" in prompt.lower() and "juego" in prompt.lower():
        response = f"{nombre_jugador}, tu partido es el sábado a las 15hs contra G. López."
    else:
        response = f"No entendí bien, {nombre_jugador}. ¿Podés reformular tu pregunta?"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
