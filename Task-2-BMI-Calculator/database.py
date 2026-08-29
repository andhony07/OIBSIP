"""
Database module for BMI Calculator
Handles SQLite connection, schema creation, record insertion, and queries.
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_records.db")


def get_db_connection() -> sqlite3.Connection:
    """
    Creates and returns a connection to the SQLite database.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to connect to database: {e}")


def init_db() -> None:
    """
    Initializes the database schema if it does not already exist.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL,
        category TEXT NOT NULL,
        recorded_at TEXT NOT NULL
    );
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database initialization failed: {e}")


def save_bmi_record(user_name: str, weight: float, height: float, bmi: float, category: str) -> bool:
    """
    Saves a new BMI calculation record to the database.

    Args:
        user_name: Name of the user
        weight: Weight in kg
        height: Height in meters
        bmi: Calculated BMI float value
        category: BMI category string

    Returns:
        bool: True if save succeeded, raises RuntimeError on failure.
    """
    insert_sql = """
    INSERT INTO bmi_records (user_name, weight, height, bmi, category, recorded_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (user_name.strip(), weight, height, round(bmi, 2), category, recorded_at))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to save record to database: {e}")


def get_all_users() -> List[str]:
    """
    Retrieves a list of distinct user names present in the database.
    """
    query_sql = "SELECT DISTINCT user_name FROM bmi_records ORDER BY user_name ASC;"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            return [row["user_name"] for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch users: {e}")


def get_user_history(user_name: Optional[str] = None) -> List[Tuple]:
    """
    Retrieves historical BMI records from the database.

    Args:
        user_name: Optional user name filter. If None or 'All Users', returns all records.

    Returns:
        List of tuples: (recorded_at, user_name, weight, height, bmi, category)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if user_name and user_name != "All Users":
                query_sql = """
                SELECT recorded_at, user_name, weight, height, bmi, category
                FROM bmi_records
                WHERE user_name = ?
                ORDER BY id ASC;
                """
                cursor.execute(query_sql, (user_name.strip(),))
            else:
                query_sql = """
                SELECT recorded_at, user_name, weight, height, bmi, category
                FROM bmi_records
                ORDER BY id ASC;
                """
                cursor.execute(query_sql)
            
            rows = cursor.fetchall()
            return [(row["recorded_at"], row["user_name"], row["weight"], row["height"], row["bmi"], row["category"]) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch history: {e}")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
