import sqlite3
from pathlib import Path

DB_PATH = Path("database/feedbacks.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_date TEXT,
            text TEXT NOT NULL,
            text_hash TEXT NOT NULL UNIQUE,
            sentiment TEXT,
            themes TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_feedback(feedback_date, text, text_hash):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO feedbacks (feedback_date, text, text_hash)
            VALUES (?, ?, ?)
        """, (feedback_date, text, text_hash))
        conn.commit()
        inserted = True
    except sqlite3.IntegrityError:
        inserted = False
    finally:
        conn.close()

    return inserted


def get_all_feedbacks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, feedback_date, text, text_hash, sentiment, themes, confidence, created_at
        FROM feedbacks
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def count_feedbacks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM feedbacks")
    count = cursor.fetchone()[0]

    conn.close()
    return count