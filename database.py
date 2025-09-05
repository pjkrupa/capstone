import psycopg2
from psycopg2 import connect
import datetime
from settings import Settings, Result

def make_db_string(settings: Settings):
    db_string = f"dbname={settings.pg_database} user={settings.pg_user} password={settings.pg_password} host={settings.pg_host} port={settings.pg_port}"
    return db_string

def drop_table(database):
    with psycopg2.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            DROP TABLE responses;
            """
        )

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
                passed_validation BOOLEAN,
                validation_errors JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

def save_response(conn: connect, result: Result, settings: Settings):
    """
    This function saves a response to the database.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO responses (run_id, model, raw_response, passed_validation, validation_errors)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (settings.run_id, settings.model, result.raw_response, result.passed_validation, result.validation_errors)
        )
    conn.commit()

def row_count(conn: connect, settings: Settings):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM responses
            WHERE run_id = %s AND model = %s;
            """,
            (settings.run_id, settings.model)
        )
        return cur.fetchone()[0]
    
def pass_count(conn: connect, settings: Settings):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM responses
            WHERE run_id = %s AND model = %s AND passed_validation = TRUE;
            """,
            (settings.run_id, settings.model)
        )
        return cur.fetchone()[0]