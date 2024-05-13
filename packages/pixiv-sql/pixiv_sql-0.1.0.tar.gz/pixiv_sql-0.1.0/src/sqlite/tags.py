import sqlite3

from pixiv_sql.lib.tags import get_tags_inserts
from sqlite.insert import upsert_into_table
from sqlite.sql import get_sql


def create_tags_table(self):
    """
    This function creates tags table in the database.

    It connects to the database, executes the SQL script to create the tables,
    commits the changes, and then closes the connection.
    """

    logger = self.logger

    # Connect to the database
    conn = sqlite3.connect(self.database)
    cur = conn.cursor()

    # Get the SQL script
    path = "./src/sql/create/tags.sql"
    sql_script = get_sql(path)

    # Execute the SQL script
    cur.executescript(sql_script)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    logger.info("[DB] 'tags' table has been created.")


def insert_tags(self, bookmarks):
    """
    This function inserts bookmarks into the 'tags' table in the database.

    Args:
        bookmarks (list): A list of dictionaries where each dictionary represents a bookmark.
    """

    # Get the SQL insert statements for the tags
    tags_inserts = get_tags_inserts(bookmarks)

    # Define the name of the table where the tags will be inserted
    table_name = "tags"

    # Define the columns of the 'tags' table
    columns = [
        "id",
        "name",
        "translated_name",
    ]

    # Call the function to upsert the tags into the table
    upsert_into_table(self, table_name, columns, tags_inserts)
