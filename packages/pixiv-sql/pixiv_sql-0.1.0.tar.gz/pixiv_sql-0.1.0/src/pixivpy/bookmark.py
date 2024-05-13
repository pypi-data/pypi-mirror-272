import time


def get_bookmarks(self):
    """
    This function retrieves a list of bookmarks for a user.
    It fetches bookmarks in a loop until there are no more bookmarks to fetch.
    If an error occurs during the fetching process, it logs the error and breaks the loop.
    """

    self.logger.info("[Start] Getting bookmark list")

    # Define a list to store bookmarks.
    bookmarks = []

    # Get a list of bookmarks.
    res = fetch_bookmarks(self)

    while res:
        try:
            # Extract the illustrations from the response.
            illusts = res.illusts
            bookmarks += illusts
            next_url = res.next_url

            # If there is a next URL, parse it and fetch the next set of bookmarks.
            if next_url:
                next_qs = self.api.parse_qs(res.next_url)
                self.logger.info(f"Next: {next_qs}")
                time.sleep(2)
                res = fetch_bookmarks(self, **next_qs)
                time.sleep(2)
            else:
                break

        except Exception as e:
            self.logger.error("Failed to get the bookmark.:", str(e))
            break

    self.logger.info("[End] Getting bookmark list")

    return bookmarks


def fetch_bookmarks(self, **kwargs):
    """
    This function fetches bookmarks for a given user ID.
    It makes a call to the Pixiv API and returns the response.
    If an error occurs during the API call, it logs the error and returns None.
    """

    try:
        # Remove 'user_id' from kwargs if it exists
        kwargs.pop("user_id", None)

        # Remove 'restrict' from kwargs if it exists
        kwargs.pop("restrict", None)

        res = self.api.user_bookmarks_illust(
            user_id=self.user_id, restrict=self.restrict, **kwargs
        )
        time.sleep(5)
        return res
    except Exception as e:
        self.logger.error("Failed to fetch bookmarks: ", str(e))
        return None
