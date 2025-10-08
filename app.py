from flask import Flask, request, jsonify
import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.contents import ChatHistory, ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

app = Flask(__name__)

# Configuración del modelo y la API key
MODEL = "gpt-4o-mini"  # Puedes usar gpt-4o o gpt-3.5-turbo
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Crear el kernel y registrar el servicio OpenAI
kernel = Kernel()
chat_service = OpenAIChatCompletion(ai_model_id=MODEL, api_key=OPENAI_API_KEY)
kernel.add_service(chat_service)

# Crear el agente (sin service_id)
agent = ChatCompletionAgent(
    name="AzureAgent",
    kernel=kernel,
    instructions="""
        Eres un asistente útil y conversacional que responde en español con explicaciones claras y breves.
        Si el usuario te saluda, responde con amabilidad.
    """
)

# Historial de conversación
history = ChatHistory()

@app.route("/")
def home():
    return "✅ Agente de Semantic Kernel desplegado correctamente en Azure Container Apps."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("prompt")

        if not user_message:
            return jsonify({"error": "Falta el campo 'prompt'"}), 400

        async def run_agent():
            # Añadir mensaje del usuario al historial
            history.add_message(ChatMessageContent(role=AuthorRole.USER, content=user_message))

            # Invocar el agente
            async for response in agent.invoke(history):
                history.add_message(response)
                return str(response.content)

        result = asyncio.run(run_agent())
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
