"""
conditional_graph.py

"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Literal

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str

def analyze_job_description(state: JobApplicationState):
    print("...Analyzing a provided job description ...")
    return {"is_suitable": len(state['job_description']) > 10}

def generate_application(state: JobApplicationState):
    print("... generatin aplication")
    return {"application": "some fake application"}

def is_suitable_condition(state: JobApplicationState) -> Literal["generate_application", END]: # type: ignore
    if state.get("is_suitable"):
        return "generate_application"
    return END

builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)

builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)

builder.add_edge("generate_application", END)

graph = builder.compile()

res = graph.invoke({"job_description":"fake_jd"})
print(res)

image_data = graph.get_graph().draw_mermaid_png()
with open("conditional_graph.png", "wb") as image_file:
    image_file.write(image_data)
print("\nImagen guardada como grafo_del_agente.png")