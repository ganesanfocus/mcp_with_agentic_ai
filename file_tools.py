# file_tools.py
import os

def write_file(filename: str, content: str):

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "success",
        "file": filename
    }
def read_file(filename: str):

    with open(filename, "r", encoding="utf-8") as f:
        return f.read()