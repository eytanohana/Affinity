from requests import Session
from requests.auth import HTTPBasicAuth

from affinity import models
from affinity import urls


class Affinity:
    def __init__(self, api_key):
        self.session = Session()
        self.session.auth = HTTPBasicAuth('', api_key)

    def get_all_lists(self) -> list[models.List]:
        response = self.session.get(urls.LISTS)
        if response.ok:
            return [models.List(**ls) for ls in response.json()]
        else:
            response.raise_for_status()
