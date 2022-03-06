import sys
import requests
import random
from pprint import pprint
from config import logger, CRAWLER_USERNAME, CRAWLER_PASSWORD
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from models.db import Student, DateFound

CREDENTIALS = (CRAWLER_USERNAME, CRAWLER_PASSWORD)


class StudentStatusMixin:
    def set_student_status(self, student_id, status):
        endpoint = 'set-student-status'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.post(
                url, 
                auth=CREDENTIALS,
                json={
                    'student_id': student_id,
                    'status': status
                    })

        r.raise_for_status()


class InstructorModelMixin:
    def set_instructor_status(self, user_id, status):
        endpoint = 'set-instructor-status'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.post(url, 
                auth=CREDENTIALS,
                json={
                    'user_id': user_id,
                    'status': status
                    })

        r.raise_for_status()

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def update_last_crawled(self, user_id):
        endpoint = 'set-user-crawled'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.post(url, 
                auth=CREDENTIALS,
                json={
                    'user_id': user_id,
                    })

        r.raise_for_status()

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def increase_search_count(self, user_id):
        endpoint = 'increase-search-count'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.post(url, 
                auth=CREDENTIALS,
                json={
                    'user_id': user_id,
                    })

        r.raise_for_status()

        if r.status_code == 200:
            return r.json()
        else:
            return None


class APIMixin(StudentStatusMixin, InstructorModelMixin):
    BASE_URL = 'http://localhost:8000/api'

    def fetch_valid_proxy(self):
        endpoint = 'get-valid-proxy'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.get(
                url,
                auth=CREDENTIALS
                )

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def fetch_next_student(self):
        endpoint = 'get-student-to-crawl'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.get(
                url,
                auth=CREDENTIALS
                )

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def fetch_watcher_info(self):
        endpoint = 'get-watcher-info'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.get(
                url,
                auth=CREDENTIALS
                )

        if r.status_code == 200:
            return r.json()
        else:
            return {}

    def ping_crawler_instance(self, crawler_id):
        endpoint = 'ping-crawler-instance'
        url = f"{self.BASE_URL}/{endpoint}/?crawler_id={crawler_id}"

        r = requests.get(
                url,
                auth=CREDENTIALS
                )

        if r.status_code == 200:
            return True
        else:
            return False

    def get_student_date_to_book(self, student_id):
        endpoint = 'get-student-date-to-book'
        url = f"{self.BASE_URL}/{endpoint}/?student_id={student_id}"

        r = requests.get(
                url,
                auth=CREDENTIALS
                )

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def fetch_crawler_instances(self, role):
        if role not in ['watch', 'book']:
            raise Exception(f'{role} is not a valid role')

        endpoint = 'get-crawler-instances'
        url = f"{self.BASE_URL}/{endpoint}/?role={role}"

        r = requests.get(
                url,
                auth=CREDENTIALS
                )

        r.raise_for_status()
        return r.json()
        if r.status_code == 200:
            return r.json()
        else:
            return {}

    def add_date_found(self, data):
        date_found = DateFound(data)
        payload = date_found.to_dict()

        endpoint = 'add-date-found'
        url = f"{self.BASE_URL}/{endpoint}/"


        r = requests.post(
                url, 
                auth=CREDENTIALS,
                json=payload
                )
        #print(r.json())
        r.raise_for_status()

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def ban_proxy(self, ip):
        endpoint = 'ban-proxy'
        url = f"{self.BASE_URL}/{endpoint}/"

        r = requests.post(
                url, 
                auth=CREDENTIALS,
                json={
                    'ip': ip,
                    })

        if r.status_code == 200:
            return r.json()
        else:
            return None


class DriverMixin:
    webdriver = webdriver
    HEADLESS = True

    def get_driver(self):
        return lambda: webdriver.Firefox(self.get_profile(), options=self.get_options())

    def init_webdriver(self):
        if self.proxy:
            logger.info(f"Proxy: {self.proxy}")
            self.webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": self.proxy,
                    #"ftpProxy": self.proxy,
                    "sslProxy": self.proxy,
                    "proxyType": "MANUAL",
            }
        else:
            logger.info("No Proxy")

    def get_profile(self):
        user_agent = self._get_user_agent()
        profile = self.webdriver.FirefoxProfile()
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',False)
        profile.set_preference("media.peerconnection.enabled", False)
        profile.set_preference("general.useragent.override", user_agent)
        profile.update_preferences()

        return profile

    def get_options(self):
        options = Options()
        if self.HEADLESS:
            options.add_argument('--headless')

        return options

    def _get_user_agent(self):
        user_agents = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                ]

        return random.choice(user_agents)



if __name__ == "__main__":
    q = APIMixin()
    print(q.get_student_date_to_book(20))
    #r = q.set_student_status(87, 5)
    #r = q.set_instructor_status(1, 3)
    #print(r)
    #print(r.json())
    #sys.exit()
    

    data = {
            'test_center_name': "Leusden (Fokkerstraat 21)" ,
            "date": "2021-09-07" ,
            "week_day": "1" ,
            "start_time": "15:00" ,
            "end_time": "15:30" ,
            "free_slots": "4" ,
            "user_id": "1" ,
            }
    
    #q.add_date_found(data)
    #q.increase_search_count('45')
    #q.ban_proxy('163.198.251.49:3128')


