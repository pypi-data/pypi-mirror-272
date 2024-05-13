def get_users_inserts(bookmarks):
    """
    This function generates a list of tuples containing user information.

    Parameters:
    bookmarks (list): A list of dictionaries where each dictionary represents a bookmark.
                      Each bookmark dictionary contains a 'user' dictionary with user details.

    Returns:
    inserts (list): A list of tuples where each tuple contains user id, name, account, and follow status.
    """

    # Create a dictionary of unique users using user id as the key
    users = {item["user"]["id"]: item["user"] for item in bookmarks}

    inserts = []

    # Iterate over the users dictionary
    for id, user in users.items():
        # Check if the user is followed, if not available default to False
        is_followed = 1 if user.get("is_followed", False) else 0

        # Append the user details as a tuple to the inserts list
        inserts.append((id, user["name"], user["account"], is_followed))

    # Return the list of user details
    return inserts
