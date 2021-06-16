import requests
from pprint import pprint
from config import logger


class APIMixin:
    BASE_URL = 'https://localhost:8001/api'

    def get_instructor_credentials(self):
        pass

