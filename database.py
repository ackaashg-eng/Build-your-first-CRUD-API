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
            ("Buy milk", False),
            ("Learn Python", False),
            ("Complete assignment", False)
        ]

        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            example_tasks
        )

        connection.commit()

    connection.close()


def get_all_tasks():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT id, title, done FROM tasks"
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


def get_task_by_id(task_id):
    connection = get_connection()

    cursor = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    )

    task = cursor.fetchone()

    connection.close()

    return task