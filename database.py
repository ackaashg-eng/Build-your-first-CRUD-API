import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        example_tasks = [
            ("Task1", True),
            ("Task2", False),
            ("Task3", False)
        ]

        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            example_tasks
        )

        connection.commit()

    connection.close()