# gemini_mcp_client.py
import asyncio
import os
from google import genai
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def main():
    server = StdioServerParameters(
        command="python",
        args=["db_mcp_server.py"]
    )

    async with stdio_client(server) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()

            tools = [{
                "function_declarations": [
                    {
                        "name": t.name,
                        "description": t.description or "MCP tool",
                        "parameters": t.inputSchema
                    }
                    for t in mcp_tools.tools
                ]
            }]
            print("Available MCP tools:", tools)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="list read tasks using MCP tool",
                config={"tools": tools}
            )

            part = response.candidates[0].content.parts[0]

            if hasattr(part, "function_call"):
                print("Executing MCP tool:", part.function_call.name)

                result = await session.call_tool(
                    part.function_call.name,
                    dict(part.function_call.args)
                )

                print("MCP result:", result)

asyncio.run(main())