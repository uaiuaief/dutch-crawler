import requests
import random
from pprint import pprint
from config import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from models.db import Student


class APIMixin:
    BASE_URL = 'http://localhost:8001/api'

    def fetch_next_student(self, user_id):
        endpoint = 'get-student-to-crawl'
        url = f"{self.BASE_URL}{endpoint}/"

        r = requests.post(url, json={'user_id': user_id})
        return r

    def fetch_instructor_to_crawl(self):
        endpoint = 'get-instructor-proxy-pair'
        url = f"{self.BASE_URL}/{endpoint}/"
        print(url)

        r = requests.get(url)

        return r

    def get_instructor_credentials(self):
        pass


class DriverMixin:
    webdriver = webdriver
    HEADLESS = False

    def get_driver(self):
        return webdriver.Firefox(self.get_profile(), options=self.get_options())

    def init_webdriver(self):
        self.proxy = '162.244.151.106:3128'
        if self.proxy:
            logger.info(f"Proxy: {self.proxy}")
            self.webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": self.proxy,
                    "ftpProxy": self.proxy,
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



a = APIMixin()
r = a.fetch_instructor_to_crawl()
print(r.json())
