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
        "Escribe una entrada extensa y exhaustiva para una enciclopedia utilizando las citas proporcionadas. La entrada debe ofrecer una descripción detallada y completa del tema, incluyendo su historia, aplicaciones, impacto, y cualquier información relevante. Asegúrate de abordar todos los aspectos pertinentes relacionados con el tema en cuestión, proporcionando una visión amplia y precisa. Además, tu entrada debe ser flexible y permitir la inclusión de detalles creativos y relevantes que enriquezcan la comprensión del tema. Pon la obra fuente de cada paráfrasis o cita textual, pero sin separarla de la discusión. no pongas un elenco de auores y citas, sino haz transiciones suaves entre los párrafos. Que sean al menos 9 párrafos. Integra las citas a lo largo de la entrada. No escribas el párrafo introductorio que explica qué fue la Escuela de Salamanca: 'La Euela de Salamanca fue un grupo de pensadores y juristas españoles del siglo XVI que se destacaron por sus contribuciones a la filosofía, la teología y el derecho. Aunque cada uno de ellos tenía sus propias perspectivas y enfoques, compartían una serie de principios y valores...' Es decir, ve directamente a la discusión de los autores y los conceptos."
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
