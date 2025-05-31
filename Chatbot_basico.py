import streamlit as st
import openai

# Configurar página
st.set_page_config(page_title="Chatbot MZF", layout="centered")
st.title("🎾 Chatbot MZF - Torneos de Tenis")
st.markdown("Conversá con el asistente para inscribirte, informar resultados y consultar sobre el torneo.")

# Cargar clave secreta de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Inicializar sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "Sos un asistente para la organización de un torneo de tenis. "
            "Tu trabajo es inscribir jugadores, registrar resultados, explicar reglas "
            "y ayudar con información sobre partidos. "
            "Si te dan un marcador, asumí que es un resultado; "
            "si te saludan, saludá cordialmente; "
            "si te preguntan por partidos, respondé con claridad. "
            "Pedí el nombre si el usuario aún no se identificó. "
            "Reconocé frases como 'anotarme', 'me inscribo', 'quiero participar', 'gané 6-4', 'juego hoy', etc."
        )}
    ]

# Mostrar historial del chat
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribí tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.6
        )
        assistant_reply = response.choices[0].message["content"]
    except Exception as e:
        assistant_reply = f"⚠️ Hubo un error al conectar con el modelo: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

