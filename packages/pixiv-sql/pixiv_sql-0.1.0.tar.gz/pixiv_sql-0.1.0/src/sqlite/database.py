import sqlite3


def connect_to_database(database: str):
    """
    Connects to the specified SQLite database.

    Args:
        database (str): The name of the database to connect to.

    Returns:
        sqlite3.Connection: The connection object to the database.
    """
    return sqlite3.connect(database)


def execute_query(conn, query: str, values: list[tuple]):
    """
    Executes a SQL query on the database.

    Args:
        conn (sqlite3.Connection): The connection object to the database.
        query (str): The SQL query to execute.
        values (list[tuple]): The values to use in the query.
    """
    cur = conn.cursor()
    cur.executemany(query, values)
    conn.commit()
