from openai import OpenAI
import streamlit as st
import pandas as pd

# Barra lateral
with st.sidebar:
    openai_api_key = st.text_input("🔑 OpenAI API Key", key="chatbot_api_key", type="password")
    uploaded_file = st.file_uploader("📂 Cargar archivo CSV", type="csv")
    "[¿No tienes una API Key? Consíguela aquí](https://platform.openai.com/account/api-keys)"

# Título de la app
st.title("📊 Chatbot basado en tu tabla de datos")
st.caption("💬 Solo responderá preguntas sobre el archivo CSV cargado")

# Variables de sesión
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Carga una tabla CSV y hazme preguntas sobre ella."}]
if "context" not in st.session_state:
    st.session_state["context"] = None

# Mostrar tabla
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Vista previa de la tabla")
    st.dataframe(df)
    st.session_state["context"] = df.to_csv(index=False)

# Mostrar historial de conversación
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta..."):
    if not openai_api_key:
        st.info("Por favor ingresa tu API Key en la barra lateral para continuar.")
        st.stop()
    if not st.session_state["context"]:
        st.warning("Debes cargar primero una tabla CSV.")
        st.stop()

    # Mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Crear cliente OpenAI
    client = OpenAI(api_key=openai_api_key)

    # Construir el prompt con contexto de tabla
    tabla_contexto = st.session_state["context"]
    question_prompt = f"""Contesta exclusivamente en base a la siguiente tabla de datos:

{tabla_contexto}

Pregunta: {prompt}
Respuesta:"""

    # Llamar al modelo
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en análisis de datos. Solo responde usando la información de la tabla que el usuario ha proporcionado."},
            {"role": "user", "content": question_prompt}
        ]
    )

    # Mostrar respuesta del chatbot
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)