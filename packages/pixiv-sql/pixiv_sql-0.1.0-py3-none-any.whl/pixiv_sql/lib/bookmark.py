from typing import Literal


def get_restrict(self, is_private: bool) -> Literal["private", "public"]:
    """
    This method determines the restriction level based on the is_private parameter.

    Parameters:
    is_private (bool): A boolean value that indicates whether the restriction is private.

    Returns:
    str: Returns 'private' if is_private is True, otherwise returns 'public'.
    """

    # Initialize the logger
    logger = self.logger

    # Determine the restriction level
    restrict = "private" if is_private else "public"

    # Log the restriction level
    logger.info(f"Restrict: {restrict}")

    # Return the restriction level
    return restrict


def get_bookmarks_insert(bookmarks) -> list[tuple]:
    """
    This function prepares the bookmark data for insertion into the database.

    Args:
        bookmarks (list): A list of dictionaries where each dictionary represents a bookmark.

    Returns:
        list[tuple]: A list of tuples where each tuple contains the bookmark data to be inserted.
    """
    # Prepare the data for each bookmark
    inserts = [
        (
            bookmark["id"],
            bookmark["title"],
            bookmark["type"],
            bookmark["caption"],
            bookmark["user"]["id"],
            bookmark["visible"],
            bookmark["illust_ai_type"],
            bookmark["illust_book_style"],
        )
        for bookmark in bookmarks  # Iterate over each bookmark
    ]

    return inserts  # Return the prepared data
