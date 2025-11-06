from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

server = {
    "excel": {
        "command": "uvx",
        "args": ["excel-mcp-server", "stdio"],
        "transport": "stdio"
    }
}

async def get_mcp_tools():
    client = MultiServerMCPClient(server)
    client.verbose = True
    return await client.get_tools()

mcp_tools = asyncio.run(get_mcp_tools())

for tool in mcp_tools:
    print(type(tool))
    print(tool)
    print("\n")
