import openai
import os

# Usa tu API Key como siempre
openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-proj-uFVEoQoZpwVpXtHugVpJ-HZ1LULcrw9VqRtOnjSq-Gyx_A8JvUcbyzXZb-Mi16R2AtwE9Yl9fxlOT3Blbk-FJl3xGtC2QvozMTdmjP8OE2czvBN7q8ZWzT-BlpMalUnm6_ZYqL9B_4LuM-FlqLrnzoVbGDPMNaVA"


from openai import OpenAI

client = OpenAI(api_key=openai.api_key)  # Cliente oficial

# Luego en tu botón de Streamlit:
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un profesor realista y útil."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=600
)

output = response.choices[0].message.content
