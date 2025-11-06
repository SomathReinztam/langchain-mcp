from mcp_agent import google_work_space_agent
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio

system_prompt = """
Eres un asistente util.
Tienes tools para manejar correos de google
"""

human_prompt="Mi correo es thomas@solenium.co , ahora dame el contenido del último correo electrónico que me llegó."

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=human_prompt)
]

initial_state = {"messages":messages}
print("\n\n"*5)
async def main():
    result = await google_work_space_agent.ainvoke(initial_state)
    for message in result["messages"]:
        message.pretty_print()

asyncio.run(main())