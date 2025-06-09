import psycopg
import os
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:
        conn = psycopg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            row_factory=dict_row,
            connect_timeout=5
        )
        return conn

    except (psycopg.Error, TimeoutError, OSError) as e:
        print("Ошибка БД", e)
        raise


def insert_result(name, score):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO results (name, score) VALUES (%s, %s)",
                (name, score)
            )
            conn.commit()


def fetch_all_results():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, score, timestamp FROM results ORDER BY timestamp DESC")
            return cur.fetchall()


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
