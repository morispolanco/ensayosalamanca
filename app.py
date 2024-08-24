import streamlit as st
import requests

# Configura la clave API en los secretos de Streamlit
api_key = st.secrets["together_ai_key"]

# Definir la URL del endpoint de la API de Together
url = "https://api.together.xyz/v1/chat/completions"

def generate_essay(citations):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Se crea la instrucción para el modelo
    instruction = (
        "Escribe un ensayo académico largo y detallado que utilice las siguientes citas como "
        "referencias. Asegúrate de analizar, discutir y conectar las ideas presentadas en las "
        "citas, proporcionando tu propia interpretación y contexto."
    )

    # Crear el mensaje para el modelo
    messages = [{"role": "system", "content": instruction}]
    for citation in citations:
        messages.append({"role": "user", "content": f"Cita: {citation}"})

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": messages,
        "max_tokens": 2048,  # Incrementar el número de tokens para permitir una discusión más larga
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["[/INST]", "</s>"],
        "stream": False  # Cambiar a True si se desea transmisión en tiempo real
    }

    response = requests.post(url, headers=headers, json=data)

    # Verifica si la respuesta es un JSON válido
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        st.error(f"Error: Respuesta no válida. Código de estado: {response.status_code}. Contenido: {response.text}")
        return

    # Verifica el código de estado HTTP
    if response.status_code == 200:
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "No se encontró contenido en la respuesta.")
    else:
        st.error(f"Error: {response_json.get('error', 'Unknown error')}")
        return

st.title("Generador de Ensayo Académico")
st.write(
    """
    Introduce las citas que deseas incluir en el ensayo. Cada cita deberá estar en una nueva línea.
    """
)

citations_input = st.text_area("Citas", height=200)
if st.button("Generar Ensayo"):
    citations = [citation.strip() for citation in citations_input.split("\n") if citation.strip()]
    if citations:
        with st.spinner("Generando ensayo..."):
            essay = generate_essay(citations)
            if essay:
                st.subheader("Ensayo Generado")
                st.write(essay)
    else:
        st.error("Por favor, introduce algunas citas.")
