import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

servers = {
    "vizro": {
        "command": "uvx",
        "args": ["vizro-mcp"],
        "transport": "stdio"
    }
}


async def get_mcp_tools():
    client = MultiServerMCPClient(servers)
    return await client.get_tools()

mcp_tools = asyncio.run(get_mcp_tools())

for tool in mcp_tools:
    print(type(tool))
    print(tool)
    print("\n")