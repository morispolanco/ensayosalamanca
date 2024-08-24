import streamlit as st
import requests
import json

# Configuración de la API de Together
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configuración del modelo y parámetros
model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
max_tokens = 2048
temperature = 0.7
top_p = 0.7
top_k = 50
repetition_penalty = 1
stop = ["[/INST]", "</s>"]
stream = True

# Función para generar el ensayo académico
def generar_ensayo(citas):
    # Preparar la solicitud a la API de Together
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Generar un ensayo académico largo a partir de las siguientes citas: " + citas}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "repetition_penalty": repetition_penalty,
        "stop": stop,
        "stream": stream
    }

    # Enviar la solicitud a la API de Together
    response = requests.post(TOGETHER_API_URL, headers=headers, json=data)

    # Procesar la respuesta de la API de Together
    if response.status_code == 200:
        ensayo = response.json()["choices"][0]["message"]["content"]
        return ensayo
    else:
        return "Error al generar el ensayo"

# Interfaz de usuario de la aplicación
st.title("Generador de ensayos académicos")
st.write("Introduce las citas para generar el ensayo:")

citas = st.text_area("Citas", height=200)

if st.button("Generar ensayo"):
    ensayo = generar_ensayo(citas)
    st.write(ensayo)
