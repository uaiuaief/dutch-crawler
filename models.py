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
    def __init__(self, driver, params, previous_page=None):
        self.previous_page = previous_page
        self.name = None
        self.params = params
        self.actions = []

        self._make_assertions(params)

        self.driver = driver
        self._set_page_actions()

        for k in params:
            self.__setattr__(k, params[k])

        
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
        logger.debug(f'{self.__class__.__name__}: next_page()')
        self._execute_page_actions()

        logger.debug(f'{self.__class__.__name__}: self.get_next_page()')
        return self.get_next_page()
    
    def get_next_page(self):
        pass

    def _execute_page_actions(self):
        for action in self.actions:
            action()

    def _set_page_actions(self, actions):
        pass

    def _make_assertions(self, params):
        assert params.get('username')
        assert params.get('password')
        assert params.get('candidate_number')
        assert params.get('password')

    @property
    def page_identifier(self):
        raise TypeError("Base Page class has no page_identifier")

    @property
    def identifiers(self):
        raise TypeError("Base Page class has no identifiers")


class LoginPage(Page):
    @property
    def page_identifier(self):
        return self.identifiers['login_input']

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

    def get_next_page(self):
        return AnnouncementsPage(self.driver, self.params, self)

    def _set_page_actions(self):
        self.actions.append(self.login)

    def login(self):
        logger.debug('login in')
        login_input = self.get_element('login_input')
        password_input = self.get_element('password_input')
        submit_button = self.get_element('submit_button')

        login_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()


class AnnouncementsPage(Page):
    @property
    def page_identifier(self):
        return ElementIdentifier(
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

    def get_next_page(self):
        return ManageExamRequestsPage(self.driver, self.params, self)

    def _set_page_actions(self):
        self.actions.append(self.click_button)

    def click_button(self):
        aanvragen = self.get_element('aanvragen')
        aanvragen.click()


class ManageExamRequestsPage(Page):
    @property
    def page_identifier(self):
        return ElementIdentifier(
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

    def get_next_page(self):
        if type(self.previous_page == 'AnnouncementsPage'):
            return SelectCandidatePage(self.driver, self.params, self)
        else:
            raise Exception('to be implemented')

    def _set_page_actions(self):
        self.actions.append(self.click_button)

    def click_button(self):
        button = self.get_element('select_candidate_button')
        button.click()


class SelectCandidatePage(Page):
    @property
    def page_identifier(self):
        return self.identifiers['candidate_number_field']

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
                ),
                'select_candidate': ElementIdentifier(
                    kind='link_text',
                    identifier='selecteren'
                )
        }

        return identifiers

    def get_next_page(self):
        raise Exception('to be implemented')
        #return SelectCandidatePage(self.driver, self.params, self)

    def _set_page_actions(self):
        self.actions.append(self.select_candidate)

    def select_candidate(self):
        cn = self.get_element('candidate_number_field')
        bd = self.get_element('birth_date_field')
        search = self.get_element('search_button')

        cn.send_keys(self.candidate_number)
        bd.send_keys(self.birth_date)
        search.click()

        candidate = self.get_element('select_candidate')
        candidate.click()

        return ManageExamRequestsPage(self.driver, self.params, self)



