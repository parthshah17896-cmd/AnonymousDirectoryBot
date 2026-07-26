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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reset_requests (
            telegram_id INTEGER PRIMARY KEY,        
            status TEXT NOT NULL,        
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        
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

def reset_selection(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE telegram_id=?",
        (telegram_id,)
    )

    conn.commit()
    conn.close()

def has_pending_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM reset_requests
        WHERE telegram_id=?
        """,
        (telegram_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row is not None and row[0] == "PENDING"

def create_reset_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO reset_requests
        (telegram_id,status)

        VALUES (?,?)
        """,
        (
            telegram_id,
            "PENDING"
        )
    )

    conn.commit()
    conn.close()

def approve_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reset_requests
        SET status='APPROVED'
        WHERE telegram_id=?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()

def reject_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reset_requests
        SET status='REJECTED'
        WHERE telegram_id=?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()

def delete_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM reset_requests
        WHERE telegram_id=?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()
