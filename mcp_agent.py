import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode


load_dotenv()
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
SERVER_AI_URL = os.getenv("SERVER_AI_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --------------------------


server = {
    "google_workspace": {
        "command": "uvx",
        "args": ["workspace-mcp"],
        "transport": "stdio", 
        "env": {
            "GOOGLE_OAUTH_CLIENT_ID": GOOGLE_OAUTH_CLIENT_ID,
            "GOOGLE_OAUTH_CLIENT_SECRET": GOOGLE_OAUTH_CLIENT_SECRET,
            "OAUTHLIB_INSECURE_TRANSPORT": "1"
        }
    }
}

async def get_mcp_tools():
    client = MultiServerMCPClient(server)
    return await client.get_tools()

mcp_tools = asyncio.run(get_mcp_tools())

# --------------------------

# model = "gpt-oss:20b"
# llm = ChatOllama(model=model, temperature=0, base_url=SERVER_AI_URL)
# llm_with_tools = llm.bind_tools(mcp_tools)

model = "gemini-2.0-flash"
llm = ChatGoogleGenerativeAI(model=model, temperature=0.7, google_api_key=GOOGLE_API_KEY)

llm_with_tools = llm.bind_tools(mcp_tools)



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

google_work_space_agent = builder.compile()
