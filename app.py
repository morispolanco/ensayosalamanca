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
        "Usando las citas proporcionadas, redacta una entrada extensa para una enciclopedia. Tu entrada debe ser detallada y abarcar los temas mencionados en las citas, ofreciendo una perspectiva amplia y precisa sobre los conceptos o eventos relacionados. Asegúrate de integrar las citas de manera coherente en el contexto de la entrada y proporcionar información adicional relevante para enriquecer la comprensión del lector sobre los temas abordados en las citas. Tu respuesta debe ser flexible y permitir la generación de una entrada única y detallada, que refleje una comprensión profunda de los temas presentados en las citas."

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

st.title("Generador de entrada de diccionario")
st.write(
    """
    Introduce las citas que deseas incluir en la entrada. Cada cita deberá estar en una nueva línea.
    """
)

citations_input = st.text_area("Citas", height=200)
if st.button("Generar entrada"):
    citations = [citation.strip() for citation in citations_input.split("\n") if citation.strip()]
    if citations:
        with st.spinner("Generando entrada..."):
            essay = generate_essay(citations)
            if essay:
                st.subheader("Entrada generada")
                st.write(essay)
    else:
        st.error("Por favor, introduce algunas citas.")
