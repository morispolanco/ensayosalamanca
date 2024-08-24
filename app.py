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
        "Redacta una entrada de enciclopedia utilizando las citas proporcionadas y compárala con las creencias de la Escuela austriaca de economía. Tu entrada debe proporcionar una explicación clara y concisa sobre los conceptos presentados en las citas, destacando las similitudes y diferencias con la perspectiva de la Escuela austriaca de economía. Además, debes asegurarte de que la comparación sea relevante y detallada, y que demuestre un entendimiento sólido de ambos enfoques económicos. Por favor, asegúrate de que tu respuesta sea informativa y precisa, y que fomente una comprensión profunda de los temas abordados. Incluye citas textuales, con referencia."
    )

    # Crear el mensaje para el modelo
    messages = [{"role": "system", "content": instruction}]
    for citation in citations:
        messages.append({"role": "user", "content": f"Cita: {citation}"})

    data = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": messages,
        "max_tokens": 3048,  # Incrementar el número de tokens para permitir una discusión más larga
        "temperature": 0.5,
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

st.title("Generador de entrada de diccionario")
st.write(
    """
    Introduce las citas que deseas incluir en la entrada. Cada cita deberá estar en una nueva línea.
    """
)

# Define los estados iniciales si no están presentes
if "citations_input" not in st.session_state:
    st.session_state.citations_input = ""
if "essay" not in st.session_state:
    st.session_state.essay = ""

citations_input = st.text_area("Citas", height=200, key="citations_input")

if st.button("Generar entrada"):
    citations = [citation.strip() for citation in st.session_state.citations_input.split("\n") if citation.strip()]
    if citations:
        with st.spinner("Generando entrada..."):
            essay = generate_essay(citations)
            if essay:
                st.session_state.essay = essay
    else:
        st.error("Por favor, introduce algunas citas.")

# Mostrar el ensayo generado, si está presente
if st.session_state.essay:
    st.subheader("Entrada generada")
    st.write(st.session_state.essay)

    st.download_button(
        label="Copiar entrada",
        data=st.session_state.essay,
        file_name="entrada_generada.txt",
        mime="text/plain"
    )
