from flask import Flask, request, jsonify
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os
import asyncio

app = Flask(__name__)

# Configuración de OpenAI
model = "gpt-4o-mini"
api_key = os.environ.get("OPENAI_API_KEY")

# Crear el kernel y registrar el servicio de OpenAI
kernel = sk.Kernel()
openai_service = OpenAIChatCompletion(service_id="openai", ai_model_id=model, api_key=api_key)
kernel.add_service(openai_service)

@app.route("/")
def home():
    return "¡Hola desde Azure Container Apps con Semantic Kernel y OpenAI!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Falta el campo 'prompt'"}), 400

        # Obtenemos el servicio de chat
        chat_service = kernel.services["openai"]

        # Usamos invoke() para generar la respuesta
        # invoke() es asíncrono, así que usamos asyncio.run() para ejecutarlo
        async def run_chat():
            return await chat_service.invoke(prompt)

        result = asyncio.run(run_chat())

        # El resultado tiene normalmente un atributo .content (dependiendo de la versión)
        response_text = getattr(result, "content", str(result))

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
