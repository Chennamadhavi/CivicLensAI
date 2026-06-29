import sqlite3

DB_NAME = "complaints.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id TEXT UNIQUE,
        complaint_text TEXT,
        analysis TEXT,
        location TEXT,
        maps_link TEXT,
        status TEXT DEFAULT 'Open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_complaint(
    complaint_id,
    complaint_text,
    analysis,
    location,
    maps_link
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO complaints (
            complaint_id,
            complaint_text,
            analysis,
            location,
            maps_link,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            complaint_id,
            complaint_text,
            analysis,
            location,
            maps_link,
            "Open"
        )
    )

    conn.commit()
    conn.close()


def get_all_complaints():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            complaint_id,
            complaint_text,
            location,
            maps_link,
            status,
            created_at
        FROM complaints
        ORDER BY created_at DESC
        """
    )

    complaints = cursor.fetchall()

    conn.close()

    return complaints


def update_status(
    complaint_id,
    status
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE complaints
        SET status = ?
        WHERE complaint_id = ?
        """,
        (
            status,
            complaint_id
        )
    )

    conn.commit()
    conn.close()


def get_complaint_by_id(
    complaint_id
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            complaint_id,
            complaint_text,
            location,
            maps_link,
            status,
            created_at
        FROM complaints
        WHERE complaint_id = ?
        """,
        (complaint_id,)
    )

    complaint = cursor.fetchone()

    conn.close()

    return complaint