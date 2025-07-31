import psycopg2
import datetime

def make_db_string(settings):
    db_string = f"dbname={settings.pg_database} user={settings.pg_user} password={settings.pg_password} host={settings.pg_host} port={settings.pg_port}"
    return db_string

def make_tables(settings):
    """
    This function creates the tables needed.
    """
    database = make_db_string(settings)
    with psycopg2.connect(database) as conn:
        cur = conn.cursor()

        # the rest of the function goes here lol

def save_response():
    """
    This function saves a response to the database.
    """
    pass




class Responses(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    run_id = Column(String)
    model = Column
    raw_response = Column(String)
    timestamp = Column(DateTime, default=datetime.now())

def create_tables():
    pass