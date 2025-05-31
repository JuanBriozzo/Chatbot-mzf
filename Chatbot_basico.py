import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="Chatbot MZF", layout="centered")
st.title("🎾 Chatbot MZF - Torneos de Tenis")
st.markdown("Conversá con el asistente para inscribirte, informar resultados y consultar sobre el torneo.")

# Tu Hugging Face API Token (reemplazá por el tuyo)
HF_TOKEN = "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"

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribí tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparar prompt con instrucciones
    system_instruction = (
        "Sos un asistente para la organización de un torneo de tenis. "
        "Inscribís jugadores, registrás resultados, explicás reglas, y respondés dudas. "
        "Reconocé saludos y frases como 'anotarme', 'quiero participar', 'gané 6-4', 'juego hoy'. "
        "Si no sabés algo, pedí que aclaren."
    )
    full_prompt = f"{system_instruction}\n\nUsuario: {prompt}\nAsistente:"

    # Llamar al modelo de Hugging Face
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-small",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": full_prompt}
        )
        result = response.json()
        assistant_reply = result[0]["generated_text"]
    except Exception as e:
        assistant_reply = f"⚠️ Hubo un error al conectar con el modelo: {e}"

    # Mostrar y guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

