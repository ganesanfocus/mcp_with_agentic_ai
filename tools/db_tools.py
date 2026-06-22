# db_tools.py
import mysql.connector
import os
from dotenv import load_dotenv
_ = load_dotenv()

def conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def read_tasks():
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    print("ROWS:", rows)   # Debug
    cur.close()
    c.close()
    return rows

def insert_task(title):
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT INTO tasks(title) VALUES(%s)", (title,))
    c.commit()
    cur.close()
    c.close()
    return {"status": "inserted"}

def update_task(task_id, title):
    c = conn()
    cur = c.cursor()
    cur.execute("UPDATE tasks SET title=%s WHERE id=%s", (title, task_id))
    c.commit()
    cur.close()
    c.close()
    return {"status": "updated"}

def delete_task(task_id):
    c = conn()
    cur = c.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    c.commit()
    cur.close()
    c.close()
    return {"status": "deleted"}