import requests
from models.db import Student


BASE_URL = 'http://localhost:8001/api/'


def fetch_next_crawl(user_id):
    endpoint = 'get-student-to-crawl'
    url = f"{BASE_URL}{endpoint}/"

    r = requests.post(url, json={'user_id': user_id})
    return r

def fetch_instructor():
