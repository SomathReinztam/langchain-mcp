"""
test_async_git_mcp_agent.py

"""

import asyncio
from async_git_mcp_agent import git_mcp_agent
from langchain_core.messages import SystemMessage, HumanMessage


GITHUB_AGENT_SYSTEM_MESSAGE = """
You are a GitHub Assistant that helps users manage their GitHub repositories and workflows.

You can help with:
- Repository management (create, fork, browse files)
- Issues and pull requests (create, review, merge)
- Code operations (search, commit, push changes)
- GitHub Actions workflows (run, monitor, debug)
- Notifications and alerts

Use the appropriate GitHub tools based on user requests. 
For complex tasks, break them down into steps and explain what you're doing along the way.

When a user needs help with GitHub, they should simply describe what they want to accomplish, 
and you'll guide them through the process using the available tools.
"""


GITHUB_AGENT_HUMAN_MESSAGE = """
Can you check my account on GitHub and look at my recent work on the sql-mine repo? 
I want to understand what I've been working on lately.
So collect information about all my recent activity and provide a brief overview in natural human language 
about my recent work.
"""

messages = [
    SystemMessage(content=GITHUB_AGENT_SYSTEM_MESSAGE),
    HumanMessage(content=GITHUB_AGENT_HUMAN_MESSAGE)
]
initial_state = {"messages": messages}


async def main():
    response = await git_mcp_agent.ainvoke(initial_state)
    print("\n" * 30)
    for message in response["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())