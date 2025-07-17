from mcp_client import MCPClient, MCPTools
import chat_assistant
from openai import OpenAI

# 1. Inicia MCP server (weather_server.py)
our_mcp_client = MCPClient(["python", "weather_server.py"])
our_mcp_client.start_server()
our_mcp_client.initialize()
our_mcp_client.initialized()

# 2. Adapta ferramentas MCP para o chat
tools = MCPTools(our_mcp_client)

# 3. Define prompt do sistema
developer_prompt = """
You help users find out the weather in their cities.
If they didn't specify a city, ask them. Make sure we always use a city.
""".strip()

# 4. Inicializa o Chat
chat = chat_assistant.ChatAssistant(
    tools=tools,
    developer_prompt=developer_prompt,
    chat_interface=chat_assistant.ChatInterface(),
    client=OpenAI()  # Certifique-se de ter configurado sua chave da OpenAI
)

# 5. Inicia o loop do chat
chat.run()
