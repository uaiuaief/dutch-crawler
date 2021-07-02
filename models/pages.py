import time
from config import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class ElementIdentifier:
    KINDS = [
            'xpath',
            'link_text',
            'class_name',
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

    def get_elements(self, name, parent=None):
        if parent:
            return self._get_elements_from_parent(name, parent)

        identifier = self.identifiers.get(name)
        if not identifier:
            raise ValueError(f'{self.__class__.__name__} has no identifier `{name}`')

        if identifier.kind == 'xpath':
            raise Exception('get multiple elements by xpath is not implemented')
        elif identifier.kind == 'link_text':
            raise Exception('get multiple elements by link_text is not implemented')
        elif identifier.kind == 'class_name':
            elements = self.driver.find_elements_by_class_name(identifier.identifier)
        else:
            raise ValueError(f"There are no identifiers of kind `{identifier.kind}`")

    def _get_elements_from_parent(self, child_name, parent):
        child_identifier = self.identifiers.get(child_name)

        if child_identifier.kind == 'xpath':
            return parent.find_elements_by_xpath(child_identifier.identifier)
        elif child_identifier.kind == 'link_text':
            return parent.find_elements_by_link_text(child_identifier.identifier)
        elif child_identifier.kind == 'class_name':
            return parent.find_elements_by_class_name(child_identifier.identifier)
        else:
            raise ValueError(f"There are no identifiers of kind `{child_identifier.kind}`")

    def get_element(self, name, parent=None):
        if parent:
            return self._get_element_from_parent(name, parent)

        identifier = self.identifiers.get(name)
        if not identifier:
            raise ValueError(f'{self.__class__.__name__} has no identifier `{name}`')

        if identifier.kind == 'xpath':
            element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, identifier.identifier)))

            return element
        elif identifier.kind == 'link_text':
            element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.LINK_TEXT, identifier.identifier)))

            return element
        elif identifier.kind == 'class_name':
            element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, identifier.identifier)))
        else:
            raise ValueError(f"There are no identifiers of kind `{identifier.kind}`")

    def _get_element_from_parent(self, child_name, parent):
        child_identifier = self.identifiers.get(child_name)

        if child_identifier.kind == 'xpath':
            return parent.find_element_by_xpath(child_identifier.identifier)
        elif child_identifier.kind == 'link_text':
            return parent.find_element_by_link_text(child_identifier.identifier)
        else:
            raise ValueError(f"There are no identifiers of kind `{child_identifier.kind}`")

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
                ),
                'candidate_number': ElementIdentifier(
                    kind='xpath',
                    identifier='//span[@id="ctl00_ctl00_DefaultContent_DefaultContent_RequestList_ctl01_RequestRow_CandidateNr"]'
                ),
                'first_row': ElementIdentifier(
                    kind='xpath',
                    identifier='//tr[@id="ctl00_ctl00_DefaultContent_DefaultContent_RequestList_ctl01_RequestRow_RowExtended"]'
                ),
                'reserveren': ElementIdentifier(
                    kind='xpath',
                    identifier='//a[@id="ctl00_ctl00_DefaultContent_DefaultContent_RequestList_ctl01_RequestRow_ReserveRequest"]'
                ),
                'dropdown': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_RefProductGroups_referenceDataCombobox_RefProductGroups_Input"]'
                ),

        }

        return identifiers

    def get_next_page(self):
        if type(self.previous_page) == AnnouncementsPage:
            return SelectCandidatePage(self.driver, self.params, self)
        else:
            return BookingPage(self.driver, self.params, self)

    def _set_page_actions(self):
        if type(self.previous_page) == AnnouncementsPage:
            self.actions.append(self.select_candidate)
        elif type(self.previous_page) == SelectCandidatePage:
            self.actions.append(self.select_test_type)
            self.actions.append(self.search_dates)
        else:
            raise TypeError(f"previous page can't be of type `{type(self.previous_page)}`")

    def select_candidate(self):
        button = self.get_element('select_candidate_button')
        button.click()

    def search_dates(self):
        button = self.get_element('search_button')
        button.click()

        candidate_number = self.get_element('candidate_number')
        candidate_number.click()

        #reserveren_button = self.get_element('reserveren', parent_name='first_row')
        reserveren_button = self.get_element('reserveren')
        reserveren_button.click()

    def select_test_type(self):
        dropdown = self.get_element('dropdown')
        dropdown.click()
        
        dropdown.send_keys('toon alles')
        dropdown.send_keys(Keys.ENTER)


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
        return ManageExamRequestsPage(self.driver, self.params, self)

    def _set_page_actions(self):
        self.actions.append(self.select_candidate)

    def select_candidate(self):
        cn = self.get_element('candidate_number_field')
        #bd = self.get_element('birth_date_field')
        search = self.get_element('search_button')

        cn.send_keys(self.candidate_number)
        #bd.send_keys(self.birth_date)
        search.click()

        candidate = self.get_element('select_candidate')
        candidate.click()


class BookingPage(Page):
    @property
    def page_identifier(self):
        return self.identifiers['booking_div']

    @property
    def identifiers(self):
        identifiers = {
                'search_button': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_Find"]'
                ),
                'booking_div': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_UPSelection"]'
                ),
                'monday': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_IncludeMondays"]'
                ),
                'tuesday': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_IncludeTuesdays"]'
                ),
                'wednesday': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_IncludeWednesdays"]'
                ),
                'thursday': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_IncludeThursdays"]'
                ),
                'friday': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_IncludeFridays"]'
                ),
                'saturday': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_IncludeSaturdays"]'
                ),
                'test_center': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_LocationSelector_referenceDataCombobox_LocationSelector_Input"]'
                ),
                'earliest_date_input': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_CapacityDateFromDatePicker_dateInput"]'
                ),
                'latest_date_input': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_CapacityDateUpToDatePicker_dateInput"]'
                ),
                'earliest_time_input': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_CapacityTimeFromField"]'
                ),
                'latest_time_input': ElementIdentifier(
                    kind='xpath',
                    identifier='//input[@id="ctl00_ctl00_DefaultContent_DefaultContent_CapacityTimeUpToField"]'
                ),
                'tbody': ElementIdentifier(
                    kind='xpath',
                    identifier='//div[@id="ctl00_ctl00_DefaultContent_DefaultContent_CapacityContainer_AvailableCapacityTab"]//table/tbody'
                ),
                'row': ElementIdentifier(
                    kind='class_name',
                    identifier='gridRow'
                ),

                #Row children:
                'date': ElementIdentifier(
                    kind='xpath',
                    identifier='.//td[2]'
                ),
                'week_day': ElementIdentifier(
                    kind='xpath',
                    identifier='.//td[3]'
                ),
                'start_time': ElementIdentifier(
                    kind='xpath',
                    identifier='.//td[4]'
                ),
                'end_time': ElementIdentifier(
                    kind='xpath',
                    identifier='.//td[5]'
                ),
                'free_slots': ElementIdentifier(
                    kind='xpath',
                    identifier='.//td[6]'
                ),
                'reserveren': ElementIdentifier(
                    kind='link_text',
                    identifier='reserveren'
                ),

                #Booking confirmation popup
                'accept_button': ElementIdentifier(
                    kind='xpath',
                    identifier='//a[@id="ctl00_ctl00_DefaultContent_DefaultContent_AcceptButton"]'
                ),
                

        }

        return identifiers

    def get_next_page(self):
        raise Exception("to be implemented")

    def _set_page_actions(self):
        self.actions.append(self.select_test_center)
        #self.actions.append(self.choose_days_to_search)
        #self.actions.append(self.fill_date_inputs)
        #self.actions.append(self.fill_time_inputs)
        self.actions.append(self.search_dates)
        self.actions.append(self.choose_date)

    def select_test_center(self):
        interval = 1
        dropdown = self.get_element('test_center')
        time.sleep(interval)
        dropdown.click()
        time.sleep(interval)
        dropdown.clear()
        time.sleep(interval)
        dropdown.send_keys('toon alles')
        time.sleep(interval)
        dropdown.send_keys(Keys.ENTER)
        time.sleep(interval)

        #dropdown.clear()
        dropdown = self.get_element('test_center')
        time.sleep(interval)
        dropdown.click()
        time.sleep(interval)
        dropdown.clear()
        time.sleep(interval)
        dropdown.send_keys(self.test_centers[0])
        time.sleep(interval)
        dropdown.send_keys(Keys.ENTER)
        time.sleep(interval)

    def choose_days_to_search(self):
        monday = self.get_element('monday')
        self.get_element('tuesday')
        self.get_element('wednesday')
        self.get_element('thursday')
        friday = self.get_element('friday')
        self.get_element('saturday')
        logger.info('choose days')


        #monday.click()
        #friday.click()

    def fill_date_inputs(self):
        earliest = self.get_element('earliest_date_input')
        latest = self.get_element('latest_date_input')
        logger.info('fill date')

        earliest.send_keys('08-07-2021')
        latest.send_keys('31-07-2021')

    def fill_time_inputs(self):
        earliest = self.get_element('earliest_time_input')
        latest = self.get_element('latest_time_input')
        logger.info('fill time')

        earliest.send_keys('12:20')
        latest.send_keys('15:35')

    def search_dates(self):
        search_button = self.get_element('search_button')
        search_button.click()

    def choose_date(self):
        tbody = self.get_element('tbody')
        rows = self.get_elements('row', tbody)
        for row in rows:
            date = self.get_element('date', row).get_attribute('textContent')
            week_day = self.get_element('week_day', row).get_attribute('textContent')
            start_time = self.get_element('start_time', row).get_attribute('textContent')
            end_time = self.get_element('end_time', row).get_attribute('textContent')
            free_slots = self.get_element('free_slots', row).get_attribute('textContent')

            reserveren_button = self.get_element('reserveren', row)

            if date == '16-08-2021':
                book_button.click()


                """ ### WARNING ###

                Clicking this button will book a date for the customer
                this can't be undone
                """
                #accept_button = self.get_element('accept_button')
                """ ### WARNING ### """

            print(date)
            print(week_day)
            print(start_time)
            print(end_time)
            print(free_slots)
            print()

