import sqlite3

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            selected_bot TEXT NOT NULL,
            selected_name TEXT NOT NULL,
            selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def user_exists(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_selection(telegram_id, selected_name, selected_bot):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (telegram_id, selected_name, selected_bot)
        VALUES (?, ?, ?)
    """, (telegram_id, selected_name, selected_bot))

    conn.commit()
    conn.close()


def get_selection(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT selected_name, selected_bot
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    result = cursor.fetchone()

    conn.close()

    return result
