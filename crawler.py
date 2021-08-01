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
from models import pages


class Crawler(APIMixin, DriverMixin):
    #URL = "https://top.cbr.nl/"
    URL = "https://top.cbr.nl/Top/LogOnView.aspx?ReturnUrl=%2ftop"

    def __init__(self, instructor, proxy):
        #self.current_page = models.LoginPage()
        self.instructor = instructor
        self.proxy = proxy
        self.init_webdriver()
        self.first_run = True

    def setup_page(self, driver):
        #with webdriver.Firefox(self.get_profile(), options=self.get_options()) as driver:
        self.driver = driver
        self.driver.get(self.URL)

        try:
            link = self.driver.find_element_by_link_text('klik hier om verder te gaan')
            link.click()
        except exceptions.NoSuchElementException:
            logger.debug('no user limit page')

        params = {
                'instructor' : self.instructor,
                }

        login_page = pages.LoginPage(self.driver, params)
        announcements_page = login_page.next_page()
        manage_exams_page_one = announcements_page.next_page()

    def _scrape(self, student, role):
        params = {
                'instructor' : self.instructor,
                'student' : student,
                'role' : role,
                }

        manage_exams_page_one = pages.ManageExamRequestsPage(
                self.driver,
                params,
                pages.AnnouncementsPage(self.driver, params))
        select_candidate_page = manage_exams_page_one.next_page()
        manage_exams_page_two = select_candidate_page.next_page()
        booking_page = manage_exams_page_two.next_page()
        booking_page.next_page()

    def book(self, student, date):
        self._scrape(student, role='book')

    def watch(self, student):
        self._scrape(student, role='watch')
        

