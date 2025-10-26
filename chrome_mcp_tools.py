import json
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


# Ruta al config del MCP de Chrome
config_path = 'chrome_mcp_config.json'
with open(config_path, "r") as f:
    config = json.load(f)

servers = config.get("mcpServers", {})
for name, server in servers.items():
    if "command" in server and "transport" not in server:
        server["transport"] = "stdio"


async def get_mcp_tools():
    client = MultiServerMCPClient(servers)
    mcp_tools = await client.get_tools()
    return mcp_tools

mcp_tools = mcp_tools = asyncio.run(get_mcp_tools())
print("\n")
print(type(mcp_tools))

for tool in mcp_tools:
    print(type(tool))
    print(tool)
    print("\n")
