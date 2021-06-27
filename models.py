from config import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ElementIdentifier:
    KINDS = [
            'xpath',
            'link_text',
    ]

    def __init__(self, kind, identifier):
        if kind not in self.KINDS:
            raise ValueError(f"`{kind}` is not a valid element kind")

        self.kind = kind
        self.identifier = identifier


class Page:
    name = None
    page_identifier = None 
    driver = None
    next_page = None

    def __init__(self, driver):
        self.driver = driver
        
    def get_element(self, name):
        identifier = self.identifiers.get(name)
        if not identifier:
            raise ValueError(f'{self.__class__.__name__} has no identifier `{name}`')

        if identifier.kind == 'xpath':
            element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, identifier.identifier)))

            return element
        elif identifier.kind == 'link_text':
            element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, identifier.identifier)))

            return element
        else:
            raise ValueError("There's no identifier of kind `{identifier.kind}`")

    def next_page(self):
        return self._do_page_actions()

    @property
    def identifiers(self):
        raise TypeError("Base Page class has no identifierxpath://top.cbr.nl/Top/LogOnView.aspx?ReturnUrl=%2ftops")


class LoginPage(Page):
    def __init__(self, driver, username, password):
        super().__init__(driver)
        self.page_identifier = self.identifiers['login_input']
        self.username = username
        self.password = password

    @property
    def identifiers(self):
        identifiers = {
                'login_input': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_ctl00_DefaultContent_DefaultContent_DefaultContent_LogOnUserName"]'
                ),
                'password_input': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_ctl00_DefaultContent_DefaultContent_DefaultContent_LogOnPassword"]'
                ),
                'submit_button': ElementIdentifier(
                    kind='xpath',
                    identifier='//a[@id="ctl00_ctl00_ctl00_DefaultContent_DefaultContent_DefaultContent_LogOn"]'
                ),
        }

        return identifiers

    def _do_page_actions(self):
        login_input = self.get_element('login_input')
        password_input = self.get_element('password_input')
        submit_button = self.get_element('submit_button')

        login_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()

        return AnnouncementsPage(self.driver)


class AnnouncementsPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_identifier = ElementIdentifier(
                kind='link_text',
                identifier='Algemeen',
        )

    @property
    def identifiers(self):
        identifiers = {
                'aanvragen': ElementIdentifier(
                    kind='link_text',
                    identifier='aanvragen'
                )
        }

        return identifiers

    def _do_page_actions(self):
        aanvragen = self.get_element('aanvragen')
        aanvragen.click()

        return ManageExamRequestsPage(self.driver)


class ManageExamRequestsPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_identifier = ElementIdentifier(
                kind='xpath',
                identifier='//div[@id="ctl00_ctl00_DefaultContent_DefaultContent_RefProductGroups_referenceDataCombobox_RefProductGroups_DropDown"]'
        )

    @property
    def identifiers(self):
        identifiers = {
                'search_button': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_FindRequests"]'
                ),
                'select_candidate_button': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_SelectCandidate"]'
                )
        }

        return identifiers

    def _do_page_actions(self):
        button = self.get_element('select_candidate_button')
        button.click()

        return SelectCandidatePage(self.driver)


class SelectCandidatePage(Page):
    def __init__(self, driver, candidate_number=None, birth_date=None):
        #assert (candidate_number or birth_date)
        super().__init__(driver)
        self.page_identifier = self.identifiers['candidate_number_field']

    @property
    def identifiers(self):
        identifiers = {
                'search_button': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_FindCandidateButton"]'
                ),
                'candidate_number_field': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_CandidateField"]'
                ),
                'birth_date_field': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_BirthdayField"]'
                )
        }

        return identifiers

    def _do_page_actions(self):
        cn = self.get_element('candidate_number_field')
        bd = self.get_element('birth_date_field')
        search = self.get_element('search_button')

        cn.send_keys('4517072525')
        bd.send_keys('27-12-1994')
        search.click()

        #return SelectCandidatePage(self.driver)
