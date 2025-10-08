using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Forzar puerto 80
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenAnyIP(80);
});

// Configuración de Semantic Kernel
var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
var deploymentName = "gpt-4o-mini";
var endpoint = "https://aleja-mghyt28b-eastus2.openai.azure.com/";

var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(deploymentName: deploymentName, endpoint: endpoint, apiKey: apiKey)
    .Build();

var chat = kernel.GetRequiredService<IChatCompletionService>();

app.MapPost("/chat", async (HttpRequest request) =>
{
    var data = await request.ReadFromJsonAsync<ChatRequest>();
    if (data == null || string.IsNullOrWhiteSpace(data.Message))
        return Results.BadRequest(new { error = "Campo 'message' requerido" });

    var history = new ChatHistory();
    history.AddUserMessage(data.Message);

    string responseText = "";
    await foreach (var chunk in chat.GetStreamingChatMessageContentsAsync(history))
    {
        responseText += chunk.Content;
    }

    return Results.Ok(new { reply = responseText });
});

app.Run();

record ChatRequest(string Message);
