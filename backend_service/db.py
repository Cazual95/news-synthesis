"""Connect to postgreSQL database."""

import psycopg2

from authentication_service import config


def create_engine():
    """Get a connection to the database."""

    db_string = f"postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/railway"

    return psycopg2.connect(dbname=config.POSTGRES_NAME, host=config.POSTGRES_HOST, port=config.POSTGRES_PORT,
                                     user=config.POSTGRES_USER, password=config.POSTGRES_PASSWORD)

def create_db() -> None:
    """Create the postgres database.

    Establish a connection based on ENV variables.
    """
    conn = get_connection()

    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE auth"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False

def create_table(
    sql_query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor
) -> None:
    """Create a table in postgres.

    Args:
        sql_query: The query to run.
        conn: The db connection to use.
        cur: The db cursor to use.
    """
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()


CREATE_USERS_TABLE = """
    CREATE TABLE user (
        id SERIAL PRIMARY KEY 
        email VARCHAR NOT NULL
        password 
        
    )
"""
