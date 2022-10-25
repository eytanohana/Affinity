from requests import Session
from requests.auth import HTTPBasicAuth


class Affinity:
    def __init__(self, api_key):
        self.session = Session()
        self.session.auth = HTTPBasicAuth('', api_key)
