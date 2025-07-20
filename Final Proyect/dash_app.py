import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"  # Asegúrate que tu API esté corriendo en esta URL

st.set_page_config(page_title="Chat Indicadores Colombia", page_icon="📊")

st.title("📊 Chat de Indicadores de Colombia")
st.write("Haz una pregunta relacionada con indicadores de desarrollo en Colombia.")

question = st.text_input("Tu pregunta:")

if st.button("Enviar"):
    if not question.strip():
        st.warning("Por favor, ingresa una pregunta válida.")
    else:
        with st.spinner("Consultando..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.success("Respuesta:")
                    st.write(data["answer"])
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error de conexión con la API: {str(e)}")
