import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def insert_example_tasks():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    count = cursor.fetchone()[0]

    if count == 0:
        connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Buy milk", False)
        )

        connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Learn Python", False)
        )

        connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Complete assignment", False)
        )

        connection.commit()

    connection.close()