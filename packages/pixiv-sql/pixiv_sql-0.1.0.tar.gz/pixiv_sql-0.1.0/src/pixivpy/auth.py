import time
from pixivpy3 import AppPixivAPI


def init_api(self) -> AppPixivAPI:
    """
    Initialize the API.

    Returns:
        AppPixivAPI: The API client.
    """

    api = AppPixivAPI()
    api.auth(refresh_token=self.refresh_token)
    time.sleep(2)

    return api
