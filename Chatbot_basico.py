import streamlit as st
import requests

# Configurar página
st.set_page_config(page_title="Chatbot MZF", layout="centered")
st.title("🎾 Chatbot MZF - Torneos de Tenis")
st.markdown("Conversá con el asistente para inscribirte, informar resultados y consultar sobre el torneo.")

# Token de Hugging Face (debe estar en Secrets)
HF_TOKEN = st.secrets["HF_TOKEN"]

# URL del modelo (puede cambiarse por otro compatible con text2text-generation o text-generation)
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-rw-1b"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Instrucción base
instruccion_sistema = (
    "Sos un asistente para la organización de un torneo de tenis. "
    "Tu trabajo es inscribir jugadores, registrar resultados, explicar reglas "
    "y ayudar con información sobre partidos. "
    "Si te dan un marcador, asumí que es un resultado; "
    "si te saludan, saludá cordialmente; "
    "si te preguntan por partidos, respondé con claridad. "
    "Pedí el nombre si el usuario aún no se identificó. "
    "Reconocé frases como 'anotarme', 'me inscribo', 'quiero participar', 'gané 6-4', 'juego hoy', etc."
)

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Función para consultar el modelo
def query_model(prompt):
    payload = {"inputs": f"Instrucción: {instruccion_sistema}\nUsuario: {prompt}\nRespuesta:"}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return result[0]["generated_text"].split("Respuesta:")[-1].strip()

# Entrada del usuario
if prompt := st.chat_input("Escribí tu mensaje..."):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener respuesta del modelo
    try:
        assistant_reply = query_model(prompt)
    except Exception as e:
        assistant_reply = f"⚠️ Hubo un error al conectar con el modelo: {e}"

    # Mostrar respuesta
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
