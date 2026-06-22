# db_mcp_server.py
from mcp.server.fastmcp import FastMCP

# import tools in server
from tools.db_tools import read_tasks, insert_task, update_task
from tools.weather_tools import get_weather
from tools.file_tools import read_file, write_file
from tools.search_tools import search_web

mcp = FastMCP("all-tools")

@mcp.tool()
def read_tasks_tool():
    """
    Retrieve all tasks from the MySQL database.
    """
    return read_tasks()

@mcp.tool()
def insert_task_tool(title: str):
    """
    Create a new task with the provided title.
    """
    return insert_task(title)

@mcp.tool()
def update_task_tool(task_id: int, title: str):
    """
    Update the title of an existing task by task ID.
    """
    return update_task(task_id, title)


@mcp.tool()
def write_file_tool(
    filename: str,
    content: str
):
    """
    Create a file and write content into it.
    """
    return write_file(filename, content)

@mcp.tool()
def weather_tool(city: str):
    """
    Get current weather information for a city.
    """
    return get_weather(city)



@mcp.tool()
def read_file_tool(filename: str):
    """
    Read content from a file.
    """
    return read_file(filename)

@mcp.tool()
def search_web_tool(topic: str):
    """
    Search the web for a topic.
    """
    return search_web(topic)

if __name__ == "__main__":
    mcp.run()
    print("MCP SERVER STARTED")