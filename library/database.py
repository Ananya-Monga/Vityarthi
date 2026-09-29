"""SQLite connection and schema setup."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "library.db"

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            total_copies INTEGER NOT NULL CHECK(total_copies >= 0),
            available_copies INTEGER NOT NULL CHECK(available_copies >= 0),
            CHECK(available_copies <= total_copies)
        );
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        );
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL REFERENCES books(id),
            member_id INTEGER NOT NULL REFERENCES members(id),
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'ISSUED'
                CHECK(status IN ('ISSUED','RETURNED'))
        );
        CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);
        """)
