import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():

    # users table

    # reset_requests table

    # profiles table

    conn.commit()    

from psycopg2.extras import RealDictCursor

def get_profiles():
    conn = psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM profiles
        WHERE is_active = TRUE
        ORDER BY id
    """)

    profiles = cur.fetchall()

    cur.close()
    conn.close()

    return profiles

def save_selection(
    telegram_id,
    profile_id,
    selected_name,
    selected_bot
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users(
            telegram_id,
            selected_profile_id,
            selected_name,
            selected_bot
        )
        VALUES(%s,%s,%s,%s)
        """,
        (
            telegram_id,
            profile_id,
            selected_name,
            selected_bot
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def user_exists(telegram_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE telegram_id=%s",
        (telegram_id,)
    )

    exists = cur.fetchone() is not None

    cur.close()
    conn.close()

    return exists
    

def get_selection(telegram_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            selected_name,
            selected_bot
        FROM users
        WHERE telegram_id=%s
        """,
        (telegram_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row
    

def reset_selection(telegram_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM users
        WHERE telegram_id=%s
        """,
        (telegram_id,)
    )

    conn.commit()

    cur.close()
    conn.close()
    

def has_pending_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM reset_requests
        WHERE telegram_id=%s
        """,
        (telegram_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row is not None and row[0] == "PENDING"

def create_reset_request(telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reset_requests (telegram_id, status)
        VALUES (%s, 'PENDING')
        ON CONFLICT (telegram_id)
        DO UPDATE SET
            status = 'PENDING',
            requested_at = CURRENT_TIMESTAMP;
    """, (telegram_id,))

    conn.commit()
    cur.close()
    conn.close()

def approve_request(telegram_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reset_requests
        SET status='APPROVED'
        WHERE telegram_id=%s
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
        WHERE telegram_id=%s
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
        WHERE telegram_id=%s
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()
