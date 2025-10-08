using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Variables de entorno
var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
var deploymentName = "gpt-4o-mini"; // ⚠️ pon aquí el nombre EXACTO de tu deployment en Azure AI Foundry
var endpoint = "https://aleja-mghyt28b-eastus2.openai.azure.com/"; // o el endpoint de tu proyecto si usas AI Foundry

// Configurar Semantic Kernel
var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(deploymentName, endpoint, apiKey)
    .Build();

var chat = kernel.GetRequiredService<IChatCompletionService>();

// Endpoint POST /chat
app.MapPost("/chat", async (ChatRequest req) =>
{
    var history = new ChatHistory();
    history.AddSystemMessage("Eres un asistente útil y conciso.");
    history.AddUserMessage(req.Message);

    string response = "";
    await foreach (var chunk in chat.GetStreamingChatMessageContentsAsync(history))
        response += chunk.Content;

    return Results.Ok(new { reply = response });
});

app.Run();

// Modelo de datos
record ChatRequest(string Message);
