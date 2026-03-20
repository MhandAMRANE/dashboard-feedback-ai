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
            judge_sentiment TEXT,
            judge_themes TEXT,
            judge_confidence REAL,
            judge_explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_unjudged_feedbacks(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, text, sentiment, themes
        FROM feedbacks
        WHERE sentiment IS NOT NULL AND judge_sentiment IS NULL
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_feedback_judge(feedback_id, judge_sentiment, judge_themes, judge_confidence, judge_explanation):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE feedbacks
        SET judge_sentiment = ?, judge_themes = ?, judge_confidence = ?, judge_explanation = ?
        WHERE id = ?
    """, (judge_sentiment, judge_themes, judge_confidence, judge_explanation, feedback_id))

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
        SELECT id, feedback_date, text, text_hash, sentiment, themes, confidence, created_at,
               judge_sentiment, judge_themes, judge_confidence, judge_explanation
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


def get_unanalyzed_feedbacks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, text
        FROM feedbacks
        WHERE sentiment IS NULL
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_feedback_analysis(feedback_id, sentiment, themes, confidence):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE feedbacks
        SET sentiment = ?, themes = ?, confidence = ?
        WHERE id = ?
    """, (sentiment, themes, confidence, feedback_id))

    conn.commit()
    conn.close()