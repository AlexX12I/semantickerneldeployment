from flask import Flask, request, jsonify
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os

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

        # Accedemos al servicio directamente desde el diccionario de servicios
        chat_service = kernel.services["openai"]

        # Ejecutar la llamada al modelo
        result = chat_service.complete(prompt=prompt)

        # El resultado es un objeto o string dependiendo de la versión
        response_text = str(result) if not isinstance(result, str) else result

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
