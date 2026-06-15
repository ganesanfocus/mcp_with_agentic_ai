# tool_executor.py
from db_tools import read_tasks, insert_task, delete_task,update_task

def execute_tool(name, args):
    if name == "read_tasks":
        return read_tasks()

    if name == "insert_task":
        return insert_task(args["title"])

    if name == "delete_task":
        return delete_task(args["task_id"])

    if name == "update_task":
        return update_task(args["task_id"], args["title"])