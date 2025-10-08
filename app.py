from flask import Flask, request, jsonify
import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent

app = Flask(__name__)

# Configuración de Azure OpenAI
DEPLOYMENT_NAME = "gpt-4o-mini"
AZURE_ENDPOINT = "https://aleja-mghyt28b-eastus2.openai.azure.com/"
AZURE_API_KEY = os.environ.get("OPENAI_API_KEY")

# Kernel y servicio de Azure OpenAI
kernel = Kernel()
chat_service = AzureChatCompletion(
    deployment_name=DEPLOYMENT_NAME,
    endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)
kernel.add_service(chat_service)  # agregamos el servicio al kernel

# Agente
agent = ChatCompletionAgent(
    name="AzureAgent",
    kernel=kernel,
    instructions="""
        Eres un asistente útil y conversacional que responde en español con explicaciones claras y breves.
        Si el usuario te saluda, responde con amabilidad.
    """
)

@app.route("/")
def home():
    return "✅ Agente Azure OpenAI desplegado correctamente"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("prompt")

        if not user_message:
            return jsonify({"error": "Falta el campo 'prompt'"}), 400

        async def run_agent():
            # Invocar el agente pasando el string
            response = await agent.invoke_async(user_message)
            return response.content

        result = asyncio.run(run_agent())
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
