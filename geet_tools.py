import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

server = {
    "'github-mcp-server'": {
        "command": "docker",
        "args": ['run', '-i', '--rm', '-e', 'GITHUB_PERSONAL_ACCESS_TOKEN', 'ghcr.io/github/github-mcp-server'],
        "transport": "stdio", 
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_PERSONAL_ACCESS_TOKEN,
        }
    }
}

async def get_mcp_tools():
    client = MultiServerMCPClient(server)
    return await client.get_tools()

mcp_tools = asyncio.run(get_mcp_tools())

for tool in mcp_tools:
    print(type(tool))
    print(tool)
    print("\n")