from sqlite.database import connect_to_database, execute_query


def insert_into_table(self, table_name: str, columns: list[str], values: list[tuple]):
    """
    Inserts values into a table in the database.

    Args:
        table_name (str): The name of the table.
        columns (list[str]): The columns to insert values into.
        values (list[tuple]): The values to insert.
    """

    # Create a logger instance
    logger = self.logger

    # Log the start of the operation
    logger.info(f"[Start] Insert {table_name} ")

    # Connect to the database
    conn = connect_to_database(self.database)

    # Define the SQL query for inserting data
    insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({', '.join(['?' for _ in columns])})
    """

    # Execute the SQL query
    execute_query(conn, insert_query, values)

    # Commit the transaction
    conn.commit()

    # Close the database connection
    conn.close()

    # Log the completion of the operation
    logger.info(f"[Completed] Insert {table_name} ")


def upsert_into_table(self, table_name: str, columns: list[str], values: list[tuple]):
    """
    Inserts or updates values into a table in the database.

    Args:
        table_name (str): The name of the table.
        columns (list[str]): The columns to insert or update values into.
        values (list[tuple]): The values to insert or update.
    """

    # Create a logger instance
    logger = self.logger

    # Log the start of the operation
    logger.info(f"[Start] Upsert {table_name} ")

    # Connect to the database
    conn = connect_to_database(self.database)

    # Define the columns to be updated
    update_columns = [
        column for column in columns if column not in ["id", "created_at"]
    ]

    # Define the SQL query for inserting or updating data
    insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({', '.join(['?' for _ in columns])})
        ON CONFLICT(id) DO UPDATE SET
        {', '.join([f'{column}=excluded.{column}' for column in update_columns])}
    """

    # Execute the SQL query
    execute_query(conn, insert_query, values)

    # Commit the transaction
    conn.commit()

    # Close the database connection
    conn.close()

    # Log the completion of the operation
    logger.info(f"[Completed] Upsert {table_name} ")
