import os
import json
import asyncio
from dotenv import load_dotenv

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

# ========================================
# CONFIGURACIÓN
# ========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#model = "openai/gpt-oss-20b"
model = "openai/gpt-oss-120b"
llm = ChatGroq(model=model, temperature=0, api_key=GROQ_API_KEY)

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature = 0, google_api_key=GOOGLE_API_KEY)


# Ruta al config del MCP de Chrome
config_path = 'chrome_mcp_config.json'
with open(config_path, "r") as f:
    config = json.load(f)

servers = config.get("mcpServers", {})
for name, server in servers.items():
    if "command" in server and "transport" not in server:
        server["transport"] = "stdio"

# ========================================
# CARGA DE TOOLS
# ========================================

async def get_mcp_tools():
    client = MultiServerMCPClient(servers)
    return await client.get_tools()

mcp_tools = asyncio.run(get_mcp_tools())
llm_with_tools = llm.bind_tools(mcp_tools)

# ========================================
# GRAFO DEL AGENTE
# ========================================

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

async def react_node(state: State) -> State:
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)

    print("🔧"*30 + " chrome_react_node")
    print("🔧"*30)
    response.pretty_print()
    print("\n" * 2)

    return {"messages": response}

tool_node = ToolNode(mcp_tools, messages_key="messages")

async def tool_node_wrapper(state: State) -> State:
    tool_response = await tool_node.ainvoke(state)
    tools = tool_response["messages"]

    print("🔧"*30 + " tool_node_wrapper")
    print("🔧"*30)
    print(f"Herramientas ejecutadas: {len(tools)}")
    print("\n")
    
    for tool in tools:
        tool.pretty_print()
        print("\n")

    return tool_response

def should_end(state: State) -> Literal["tool_node_wrapper", END]: # type: ignore
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tool_node_wrapper"
    return END

builder = StateGraph(State)
builder.add_node("react_node", react_node)
builder.add_node("tool_node_wrapper", tool_node_wrapper)
builder.add_edge(START, "react_node")
builder.add_edge("tool_node_wrapper", "react_node")
builder.add_conditional_edges("react_node", should_end)

chrome_agent = builder.compile()
