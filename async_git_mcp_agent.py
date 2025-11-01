import os
import json
import asyncio
from dotenv import load_dotenv

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

# ====================================================
# CONFIGURACIÓN INICIAL
# ====================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-20b"
llm = ChatGroq(model=model, temperature=0, api_key=GROQ_API_KEY)

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


# ====================================================
# DEFINICIÓN DE TOOLS (asíncrona)
# ====================================================

async def get_mcp_tools():
    client = MultiServerMCPClient(server)
    mcp_tools = await client.get_tools()
    return mcp_tools

# Ejecutar carga de tools una vez
mcp_tools = asyncio.run(get_mcp_tools())

# LLM con tools enlazadas
llm_with_tools = llm.bind_tools(mcp_tools)


# ====================================================
# ESTADO Y NODOS DEL GRAFO
# ====================================================

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


async def react_node(state: State) -> State:
    """Nodo principal del agente LLM."""
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)

    print("xx"*30 + " react_node")
    print("xx"*30)
    messages[-1].pretty_print()
    print("\n" * 2)

    return {"messages": response}


tool_node = ToolNode(mcp_tools, messages_key="messages")

async def tool_node_wrapper(state: State) -> State:
    """Nodo para ejecución de herramientas."""
    tool_response = await tool_node.ainvoke(state)
    tools = tool_response["messages"]

    print("xx"*30 + " tool_node_wrapper")
    print("xx"*30)
    print("\n")
    print(f"len tools: {len(tools)}")
    print("\n")
    for tool in tools:
        tool.pretty_print()
        print("\n")
    print("\n" * 1)

    return tool_response


def should_end(state: State) -> Literal["tool_node_wrapper", END]:  # type: ignore
    """Decide si continuar con herramientas o finalizar."""
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tool_node_wrapper"
    return END


# ====================================================
# CONSTRUCCIÓN DEL GRAFO DE ESTADOS
# ====================================================

builder = StateGraph(State)
builder.add_node("react_node", react_node)
builder.add_node("tool_node_wrapper", tool_node_wrapper)

builder.add_edge(START, "react_node")
builder.add_edge("tool_node_wrapper", "react_node")
builder.add_conditional_edges("react_node", should_end)

git_mcp_agent = builder.compile()


