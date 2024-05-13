import sqlite3

from pixiv_sql.lib.bookmark import get_bookmarks_insert
from sqlite.insert import upsert_into_table
from sqlite.sql import get_sql


def create_bookmarks_table(self):
    """
    This function creates bookmarks table in the database.

    It connects to the database, executes the SQL script to create the tables,
    commits the changes, and then closes the connection.
    """

    logger = self.logger

    # Connect to the database
    conn = sqlite3.connect(self.database)
    cur = conn.cursor()

    # Get the SQL script
    path = "./src/sql/create/bookmarks.sql"
    sql_script = get_sql(path)

    # Execute the SQL script
    cur.executescript(sql_script)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    logger.info("[DB] 'bookmarks' table has been created.")


def insert_bookmarks(self, bookmarks):
    """
    This function inserts bookmarks into the 'bookmarks' table in the database.

    Args:
        bookmarks (list): A list of dictionaries where each dictionary represents a bookmark.
    """

    # Get the SQL insert statements for the bookmarks
    bookmarks_inserts = get_bookmarks_insert(bookmarks)

    # Define the name of the table where the bookmarks will be inserted
    table_name = "bookmarks"

    # Define the columns of the 'bookmarks' table
    columns = [
        "id",
        "title",
        "type",
        "caption",
        "user_id",
        "visible",
        "illust_ai_type",
        "illust_book_style",
    ]

    # Call the function to upsert the bookmarks into the table
    upsert_into_table(self, table_name, columns, bookmarks_inserts)
