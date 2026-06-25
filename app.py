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
            print(tools)

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
            print("Response:", part.text)

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
    <head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #667eea; }
        .card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); width: 480px; }
        h2 { color: #333; margin-bottom: 24px; font-size: 22px; }
        input { width: 100%; padding: 12px 16px; border: 2px solid #eee; border-radius: 8px; font-size: 15px; outline: none; transition: border 0.2s; }
        input:focus { border-color: #667eea; }
        button { width: 100%; margin-top: 12px; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #5a6fd6; }
    </style>
    </head>
    <body>
        <div class="card">
            <h2>🤖 MCP Task Assistant</h2>
            <form method="post">
                <input type="text" name="prompt" placeholder="Ask me anything...">
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
async def submit(prompt: str = Form(...)):
    result = await process_prompt(prompt)
    return f"""
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }}
        body {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #667eea; }}
        .card {{ background: white; padding: 40px; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); width: 480px; }}
        h2 {{ color: #333; margin-bottom: 24px; font-size: 22px; }}
        input {{ width: 100%; padding: 12px 16px; border: 2px solid #eee; border-radius: 8px; font-size: 15px; outline: none; transition: border 0.2s; }}
        input:focus {{ border-color: #667eea; }}
        button {{ width: 100%; margin-top: 12px; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; transition: background 0.2s; }}
        button:hover {{ background: #5a6fd6; }}
        .result {{ margin-top: 24px; padding: 16px; background: #f4f4f4; border-radius: 8px; border-left: 4px solid #667eea; }}
        pre {{ white-space: pre-wrap; word-break: break-word; font-size: 14px; color: #444; }}
    </style>
    </head>
    <body>
        <div class="card">
            <h2>🤖 MCP Task Assistant</h2>
            <form method="post">
                <input type="text" name="prompt" value="{prompt}" placeholder="Ask me anything...">
                <button type="submit">Submit</button>
            </form>
            <div class="result">
                <pre>{result}</pre>
            </div>
        </div>
    </body>
    </html>
    """