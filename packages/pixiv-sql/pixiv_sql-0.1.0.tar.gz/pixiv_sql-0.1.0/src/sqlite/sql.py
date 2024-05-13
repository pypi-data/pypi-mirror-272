def get_sql(path: str):
    """
    This method reads a SQL script from a file and returns it as a string.

    Args:
        path (str): The path to the SQL script file.

    Returns:
        str: The SQL script read from the file.
    """

    # Open the file in read mode
    with open(path, "r") as f:
        # Read the SQL script
        sql_script = f.read()

    # Return the SQL script
    return sql_script
