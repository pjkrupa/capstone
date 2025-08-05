from psycopg2 import connect
import datetime
from settings import Settings

def make_db_string(settings: Settings):
    db_string = f"dbname={settings.pg_database} user={settings.pg_user} password={settings.pg_password} host={settings.pg_host} port={settings.pg_port}"
    print(db_string)
    return db_string

def make_tables(conn: connect, settings: Settings):
    """
    This function creates the tables needed.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS responses (
                id SERIAL PRIMARY KEY,
                run_id VARCHAR,
                model VARCHAR,
                raw_response JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

def save_response(conn: connect, raw_response: str, settings: Settings):
    """
    This function saves a response to the database.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO responses (run_id, model, raw_response)
            VALUES (%s, %s, %s);
            """,
            (settings.run_id, settings.model, raw_response)
        )

def row_count(conn: connect, settings: Settings):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM responses
            WHERE run_id = %s;
            """,
            (settings.run_id,)
        )
        return cur.fetchone()[0]