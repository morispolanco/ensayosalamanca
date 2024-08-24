import streamlit as st
import requests

# Configura la clave API en los secretos de Streamlit
api_key = st.secrets["together_ai_key"]

# Definir la URL del endpoint de la API de Together
url = "https://api.together.xyz/v1/generate"

def generate_essay(citations):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "input": {
            "format": "essay",
            "citations": citations,
        }
    }

    response = requests.post(url, headers=headers, json=data)

    # Verifica si la respuesta es un JSON válido
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        return f"Error: Respuesta no válida. Código de estado: {response.status_code}. Contenido: {response.text}"

    # Verifica el código de estado HTTP
    if response.status_code == 200:
        return response_json.get("output", "No se encontró contenido en la respuesta.")
    else:
        return f"Error: {response_json.get('error', 'Unknown error')}"

st.title("Generador de Ensayo Académico")
st.write(
    """
    Introduce las citas que deseas incluir en el ensayo. Cada cita deberá estar en una nueva línea.
    """
)

citations_input = st.text_area("Citas", height=200)
if st.button("Generar Ensayo"):
    citations = citations_input.split("\n")
    if citations:
        with st.spinner("Generando ensayo..."):
            essay = generate_essay(citations)
            st.subheader("Ensayo Generado")
            st.write(essay)
    else:
        st.error("Por favor, introduce algunas citas.")
