from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
model = ChatOpenAI(model="gpt-4o")


async def main():
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["mcp_servers/math_server.py"],
                "transport": "stdio",
            },
            # "weather": {
            #     # make sure you start your weather server on port 8000
            #     "url": "http://localhost:8000/sse",
            #     "transport": "sse",
            # }
            "weather": {
                "command": "python",
                "args": ["mcp_servers/weather_server.py"],
                "transport": "stdio",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        math_response = await agent.ainvoke({"messages": "Hello"})
        # weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
        print(math_response['messages'][-1].content)
        ai_message_with_tool = math_response['messages'][1]
        if ai_message_with_tool.tool_calls:
            print(f"Tool name: {ai_message_with_tool.tool_calls[0]['name']}")
        # print(weather_response)

if __name__ == "__main__":
    asyncio.run(main())
