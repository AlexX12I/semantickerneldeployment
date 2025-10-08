from flask import Flask, request, jsonify
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os
import asyncio

app = Flask(__name__)

# Configuración de OpenAI
model = "gpt-4o-mini"   # Puedes usar gpt-4o, gpt-3.5-turbo, etc.
api_key = os.environ.get("OPENAI_API_KEY")

# Crear kernel y añadir el servicio de OpenAI
kernel = sk.Kernel()
chat_service = OpenAIChatCompletion(ai_model_id=model, api_key=api_key)
kernel.add_service(chat_service)

@app.route("/")
def home():
    return "¡Hola desde Azure Container Apps con Semantic Kernel y OpenAI!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Falta el campo 'prompt'"}), 400

        async def chat_response():
            # Creamos una sesión de chat (ChatHistory)
            chat = kernel.create_new_chat()
            chat.add_user_message(prompt)

            # Ejecutamos el chat con el servicio configurado
            response = await kernel.services.get("chat_completion").complete_chat(chat)

            # `response` es un ChatMessageContent, el texto está en .content
            return response.content

        result = asyncio.run(chat_response())

        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
