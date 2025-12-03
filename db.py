import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')


def _is_postgres():
    return bool(DATABASE_URL and DATABASE_URL.startswith('postgres'))


def get_connection():
    """Return a new DB connection. Postgres if DATABASE_URL set, else sqlite3."""
    if _is_postgres():
        try:
            import psycopg2
            return psycopg2.connect(DATABASE_URL)
        except Exception:
            raise
    else:
        # use file-based sqlite in project root
        db_path = Path(__file__).parent / 'blog.db'
        return sqlite3.connect(str(db_path))


def _convert_params(query, params):
    """Convert sqlite-style '?' placeholders to psycopg2 '%s' placeholders when needed."""
    if _is_postgres():
        # naive replacement: replace all ? with %s
        converted = ''
        i = 0
        for ch in query:
            if ch == '?':
                converted += '%s'
            else:
                converted += ch
        return converted, params
    return query, params


def fetchall(query, params=None):
    params = params or ()
    q, p = _convert_params(query, params)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(q, p)
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()


def fetchone(query, params=None):
    params = params or ()
    q, p = _convert_params(query, params)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(q, p)
        row = cur.fetchone()
        return row
    finally:
        conn.close()


def execute(query, params=None, commit=True):
    params = params or ()
    q, p = _convert_params(query, params)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(q, p)
        if commit:
            conn.commit()
        return cur
    finally:
        conn.close()
