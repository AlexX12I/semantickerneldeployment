from flask import Flask, request, jsonify
import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.contents import ChatHistory, ChatMessageContent, AuthorRole

app = Flask(__name__)

# Configuración de Azure OpenAI
DEPLOYMENT_NAME = "gpt-4o-mini"
AZURE_ENDPOINT = "https://aleja-mghyt28b-eastus2.openai.azure.com/"
AZURE_API_KEY = os.environ.get("OPENAI_API_KEY")

# Crear el Kernel y agregar el servicio
kernel = Kernel()
chat_service = AzureChatCompletion(
    deployment_name=DEPLOYMENT_NAME,
    endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)
kernel.add_service(chat_service)

# Crear el agente
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
    return "✅ Agente Azure OpenAI desplegado correctamente"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("prompt")
    if not user_message:
        return jsonify({"error": "Falta el campo 'prompt'"}), 400

    async def run_agent():
        history.add_message(ChatMessageContent(role=AuthorRole.USER, content=user_message))

        async for response in agent.invoke(history):
            history.add_message(ChatMessageContent(role=AuthorRole.ASSISTANT, content=response.content))
            return str(response.content)

    try:
        result = asyncio.run(run_agent())
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
