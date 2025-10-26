import math
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Sequence, Literal


def mocked_google_search(query: str) -> str:
  print(f"CALLED GOOGLE_SEARCH with query={query}")
  return "Donald Trump is a president of USA and he's 78 years old"

def mocked_calculator(expression: str) -> float:
  print(f"CALLED CALCULATOR with expression={expression}")
  if "sqrt" in expression:
    return math.sqrt(78*132)
  return 78*132



calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Computes mathematical expressions",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "title": "expression",
                    "description": "A mathematical expression to be evaluated by a calculator"
                }
            },
            "required": ["expression"]
        }
    }
}

search_tool = {
    "type": "function",
    "function": {
        "name": "google_search",
        "description": "Returns about common facts, fresh events and news from Google Search engine based on a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "title": "search_query",
                    "description": "Search query to be sent to the search engine"
                }
            },
            "required": ["query"]
        }
    }
}


llm = ChatGoogleGenerativeAI(
     model='gemini-2.0-flash',
     temperature = 0
)


llm_with_tools = llm.bind(tools=[calculator_tool, search_tool])



class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def invoke_llm(state: State):
   res = llm_with_tools.invoke(state["messages"])
   return {"messages":res}


def call_tools(state: State):

   last_message = state["messages"][-1]
   tool_calls = last_message.tool_calls

   new_messages = []

   for tool_call in tool_calls:
    if tool_call["name"] == "google_search":
        tool_result = mocked_calculator(**tool_call['args'])
        new_messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))

    elif tool_call["name"] == "calculator":
       tool_result =  mocked_calculator(**tool_call['args'])
       new_messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call['id']))
    else:
       raise ValueError(f"Tool {tool_call['name']} is not defined!")

    return {"messages":new_messages}


def should_run_tools(state : State) -> Literal["call_tools", END]: # type: ignore
   last_message = state["messages"][-1]
   if last_message.tool_calls:
      return "call_tools"
   return END


builder = StateGraph(State)
builder.add_node("invoke_llm", invoke_llm)
builder.add_node("call_tools", call_tools)

builder.add_edge(START, "invoke_llm")
builder.add_conditional_edges("invoke_llm", should_run_tools)
builder.add_edge("call_tools", "invoke_llm")

builder.compile()


system_prompt = (
    "Always use a calculator for mathematical computations, and use Google Search "
    "for information about common facts, fresh events and news. Do not assume anything, keep in "
    "mind that things are changing and always "
    "check yourself with external sources if possible."
)

human_prompt = ("age of current US president")

message = ChatPromptTemplate.from_messages([
   ("system", system_prompt),
   ("human", human_prompt)
])

initial_state = {"messages":message}