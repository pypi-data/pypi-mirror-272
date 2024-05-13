import hashlib


def get_tags_inserts(bookmarks) -> list:
    """
    Generate a list of tuples containing unique index, name, and translated name for each tag in the bookmarks.

    Parameters:
    bookmarks (list): A list of bookmarks where each bookmark is a dictionary containing 'id' and 'tags'.

    Returns:
    inserts (list): A list of tuples where each tuple contains unique index, name, and translated name of a tag.
    """
    all_tags = [tag for item in bookmarks for tag in item["tags"]]
    tags = [dict(t) for t in set(tuple(d.items()) for d in all_tags)]
    inserts = []
    for tag in tags:
        unique_index = generate_unique_index(tag["name"])
        inserts.append((unique_index, tag["name"], tag["translated_name"]))

    return inserts


def get_bookmarks_tags_inserts(bookmarks) -> list:
    """
    Generate a list of tuples containing bookmark id and unique index for each tag in the bookmarks.

    Parameters:
    bookmarks (list): A list of bookmarks where each bookmark is a dictionary containing 'id' and 'tags'.

    Returns:
    inserts (list): A list of tuples where each tuple contains bookmark id and unique index of a tag.
    """
    inserts = []
    for item in bookmarks:
        for tag in item["tags"]:
            unique_index = generate_unique_index(tag["name"])
            inserts.append((item["id"], unique_index))

    return inserts


def generate_unique_index(name) -> int:
    """
    Generate a unique index for a given name using SHA-256 hashing.

    Parameters:
    name (str): The name for which to generate a unique index.

    Returns:
    int: The unique index generated from the name.
    """
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16) % 10**8
