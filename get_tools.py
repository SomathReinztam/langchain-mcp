"""
repo:
https://github.com/taylorwilsdon/google_workspace_mcp

"""

from dotenv import load_dotenv
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


load_dotenv()
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

server = {
    "google_workspace": {
        "command": "uvx",
        "args": ["workspace-mcp"],
        "transport": "stdio",  # 👈 Añadido aquí
        "env": {
            "GOOGLE_OAUTH_CLIENT_ID": GOOGLE_OAUTH_CLIENT_ID,
            "GOOGLE_OAUTH_CLIENT_SECRET": GOOGLE_OAUTH_CLIENT_SECRET,
            "OAUTHLIB_INSECURE_TRANSPORT": "1"
        }
    }
}

#print(server)

async def get_mcp_tools():
    client = MultiServerMCPClient(server)
    return await client.get_tools()

mcp_tools = asyncio.run(get_mcp_tools())

for tool in mcp_tools:
    print(type(tool))
    print(tool)
    print("\n")