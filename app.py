from flask import Flask, request, jsonify
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os

app = Flask(__name__)

# Configurar el Kernel
kernel = sk.Kernel()
kernel.add_text_completion_service(
    "openai-gpt4",
    OpenAIChatCompletion("gpt-4", api_key=os.getenv("6mxPxkUXYkwZ1AMb7OqjP1zFX0BvATv3rB5FT6VJG3IgIGygsTb0JQQJ99BJAC5RqLJXJ3w3AAABACOGQq76"))
)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    completion = kernel.services.get("openai-gpt4").complete(prompt)
    return jsonify({"response": completion})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
