from chrome_mcp_agent import chrome_agent
from langchain_core.messages import SystemMessage, HumanMessage
from myPrompts import SYSTEM_MESSAGE, HUMAN_MESSAGE_3
import asyncio


messages = [
    SystemMessage(content=SYSTEM_MESSAGE),
    HumanMessage(content=HUMAN_MESSAGE_3)
]

initial_state = {"messages":messages}

async def main():
    result = await chrome_agent.ainvoke(initial_state)
    for message in result["messages"]:
        message.pretty_print()

asyncio.run(main())