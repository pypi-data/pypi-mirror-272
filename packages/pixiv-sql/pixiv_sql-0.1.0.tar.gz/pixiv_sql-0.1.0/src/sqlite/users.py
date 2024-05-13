import sqlite3

from pixiv_sql.lib.user import get_users_inserts
from sqlite.insert import upsert_into_table
from sqlite.sql import get_sql


def create_users_table(self):
    """
    This function creates users table in the database.

    It connects to the database, executes the SQL script to create the tables,
    commits the changes, and then closes the connection.
    """

    logger = self.logger

    # Connect to the database
    conn = sqlite3.connect(self.database)
    cur = conn.cursor()

    # Get the SQL script
    path = "./src/sql/create/users.sql"
    sql_script = get_sql(path)

    # Execute the SQL script
    cur.executescript(sql_script)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    logger.info("[DB] 'users' table has been created.")


def insert_users(self, bookmarks):
    """
    This function inserts bookmarks into the 'users' table in the database.

    Args:
        bookmarks (list): A list of dictionaries where each dictionary represents a bookmark.
    """

    # Get the SQL insert statements for the users
    users_inserts = get_users_inserts(bookmarks)

    # Define the name of the table where the users will be inserted
    table_name = "users"

    # Define the columns of the 'users' table
    columns = [
        "id",
        "name",
        "account",
        "is_followed",
    ]

    # Call the function to upsert the users into the table
    upsert_into_table(self, table_name, columns, users_inserts)
