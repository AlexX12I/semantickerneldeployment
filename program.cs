using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
var deploymentName = "gpt-4o-mini";
var endpoint = "https://aleja-mghyt28b-eastus2.openai.azure.com/";

var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(
        deploymentName: deploymentName,
        endpoint: endpoint,
        apiKey: apiKey
    )
    .Build();

var chat = kernel.GetRequiredService<IChatCompletionService>();
const string systemPrompt = "Eres un asistente útil y conciso.";

Console.WriteLine("Ask me anything (Enter para salir)");

while (true)
{
    string? user = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(user)) break;

    var history = new ChatHistory();
    history.AddSystemMessage(systemPrompt);
    history.AddUserMessage(user);

    await foreach (var chunk in chat.GetStreamingChatMessageContentsAsync(history))
        Console.Write(chunk.Content);

    Console.WriteLine();
}
