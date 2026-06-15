# app.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import asyncio
import os

from google import genai
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
from dotenv import load_dotenv

load_dotenv()
from research_agent import research_topic

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


async def process_prompt(prompt: str):

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
                        "description": t.description or "MCP Tool",
                        "parameters": t.inputSchema
                    }
                    for t in mcp_tools.tools
                ]
            }]

            if prompt.lower().startswith("research "):

                topic = prompt[9:].strip()

                result = await research_topic(
                    session,
                    client,
                    topic
                )

                return (
                    f"File Created: {result['filename']}\n\n"
                    f"{result['summary']}"
                )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"tools": tools}
            )

            part = response.candidates[0].content.parts[0]

            if hasattr(part, "function_call"):
                print("Function called:", part.function_call.name)
                print("Arguments:", dict(part.function_call.args))

                result = await session.call_tool(
                    part.function_call.name,
                    dict(part.function_call.args)
                )

                all_tasks = []

                for item in result.content:
                    all_tasks.append(item.text)

                return "\n\n".join(all_tasks)
                # return result.content[0].text

            return response.text


@app.get("/", response_class=HTMLResponse)
async def home():

    return """
    <html>
        <body>
            <h2>MCP Task Assistant</h2>

            <form method="post">
                <input type="text"
                       name="prompt"
                       style="width:400px">

                <button type="submit">
                    Submit
                </button>
            </form>
        </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
async def submit(prompt: str = Form(...)):

    result = await process_prompt(prompt)

    return f"""
    <html>
        <body>
            <h2>MCP Task Assistant</h2>

            <form method="post">
                <input type="text"
                       name="prompt"
                       value="{prompt}"
                       style="width:400px">

                <button type="submit">
                    Submit
                </button>
            </form>

            <hr>

            <pre>{result}</pre>

        </body>
    </html>
    """