import sqlite3

from pixiv_sql.lib.tags import get_bookmarks_tags_inserts
from sqlite.insert import insert_into_table
from sqlite.sql import get_sql


def create_bookmarks_tags_table(self):
    """
    This function creates bookmarks_tags table in the database.

    It connects to the database, executes the SQL script to create the tables,
    commits the changes, and then closes the connection.
    """

    logger = self.logger

    # Connect to the database
    conn = sqlite3.connect(self.database)
    cur = conn.cursor()

    # Get the SQL script
    path = "./src/sql/create/bookmarks_tags.sql"
    sql_script = get_sql(path)

    # Execute the SQL script
    cur.executescript(sql_script)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    logger.info("[DB] 'bookmarks_tags' table has been created.")


def insert_bookmarks_tags(self, bookmarks):
    """
    This function inserts bookmarks into the 'bookmarks_tags' table in the database.

    Args:
        bookmarks (list): A list of dictionaries where each dictionary represents a bookmark.
    """

    # Get the SQL insert statements for the bookmarks_tags
    bookmarks_tags_inserts = get_bookmarks_tags_inserts(bookmarks)

    # Define the name of the table where the bookmarks_tags will be inserted
    table_name = "bookmarks_tags"

    # Define the columns of the 'bookmarks_tags' table
    columns = [
        "bookmark_id",
        "tag_id",
    ]

    # Call the function to insert the bookmarks_tags into the table
    insert_into_table(self, table_name, columns, bookmarks_tags_inserts)
