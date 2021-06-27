import random
from mixins import APIMixin, DriverMixin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from captcha_solver import solver
from config import logger
import models


class Crawler(APIMixin, DriverMixin):
    #URL = "https://top.cbr.nl/"
    URL = "https://top.cbr.nl/Top/LogOnView.aspx?ReturnUrl=%2ftop"

    def __init__(self):
        #self.current_page = models.LoginPage()
        self.instructor = None
        self.proxy = None
        self.init_webdriver()

    def scrape(self):
        self.driver = self.get_driver()
        self.driver.get(self.URL)

        try:
            link = self.driver.find_element_by_link_text('klik hier om verder te gaan')
            link.click()
        except exceptions.NoSuchElementException:
            logger.debug('no user limit page')

        username = "Kirmit91"
        password = "Rijswijk123!"

        login_page = models.LoginPage(self.driver, username, password)
        announcements_page = login_page.next_page()
        manage_exams_page = announcements_page.next_page()
        select_candidate_page = manage_exams_page.next_page()
        select_candidate_page.next_page()

        print(self.driver.current_url)
    
    def get_current_page(self):
        pass

