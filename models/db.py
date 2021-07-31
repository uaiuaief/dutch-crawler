import json
from pprint import pprint
from datetime import datetime


def asdict(obj):
    if isinstance(obj, list):
        return [asdict(element) for element in obj]

    if not hasattr(obj, '__dict__'):
        return str(obj)

    result = {}
    for attr in dir(obj): 
        attr_value = getattr(obj, attr)
        if not attr.startswith('_') and not callable(attr_value):
            result[attr] = asdict(attr_value)

    return result


class BaseClass:
    def to_json(self):
        return json.dumps(asdict(self), indent=4)
    
    def to_dict(self):
        return asdict(self)


class Instructor(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        profile = data['profile']

        self.first_name = profile['first_name']
        self.last_name = profile['last_name']
        self.test_center = profile['test_center']
        self.gov_username = profile['gov_username']
        self.gov_password = profile['gov_password']
        self.students = profile['students']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def test_center(self):
        return self._test_center

    @test_center.setter
    def test_center(self, data):
        self._test_center = TestCenter(data)
    
    @property
    def students(self):
        return self._students

    @students.setter
    def students(self, students):
        arr = [Student(each) for each in students]

        self._students = arr


class Student(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        self.candidate_number = data['candidate_number']
        self.birth_date = data['birth_date']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.test_type = data['test_type']
        self.date_to_book = data['date_to_book']
        self.days_to_skip = data['days_to_skip']
        self.status = data['status']
        self.search_range = data['search_range']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def date_to_book(self):
        return self._date_to_book

    @date_to_book.setter
    def date_to_book(self, value):
        self._date_to_book = DateFound(value)

    @property
    def days_to_skip(self):
        return self._days_to_skip

    @days_to_skip.setter
    def days_to_skip(self, days: str):
        if days is None:
            self._days_to_skip = []
            return

        has_comma = days.find(',')
        if has_comma > 0:
            days_list = [int(day) for day in days.split(',') if self._is_valid_day(int(day))] 
        else:
            if self._is_valid_day(int(days)):
                days_list = [int(days)]
            else:
                days_list = []

        self._days_to_skip = days_list

    def _is_valid_day(self, day):
        if 0 < day <= 31:
            return True
        else:
            return False


class TestCenter(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class DateFound(BaseClass):
    def __init__(self, data):
        self.test_center_name = data['test_center_name']
        self.date = data['date']
        self.test_type = data['test_type']
        self.week_day = data['week_day']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.free_slots = data['free_slots']
        self.user_id = data['user_id']

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = datetime.strptime(value, "%Y-%m-%d").date()

if __name__ == "__main__":
    data = {
            "id": 1,
            "email": "john@john.com",
            "profile": {
                "first_name": "John",
                "last_name": "Galt",
                "test_center": {
                    "id": 89,
                    "created_at": "2021-07-09T17:42:37.428286Z",
                    "last_modified": "2021-07-09T17:42:37.428339Z",
                    "name": "Leusden (Fokkerstraat 21)"
                },
                "mobile_number": "999999999999999",
                "gov_username": "Kirmit91",
                "gov_password": "Rijswijk123!",
                "student_limit": 100,
                "students": [
                    {
                        "id": 76,
                        "created_at": "2021-07-08T23:08:04.801303Z",
                        "last_modified": "2021-07-09T18:56:02.245580Z",
                        "candidate_number": "d2d123",
                        "birth_date": "2021-05-11",
                        "first_name": "Chester",
                        "last_name": "Bennington",
                        "test_type": "B",
                        "search_range": "1",
                        "days_to_skip": '1,13,32,31,0',
                        "last_crawled": "2021-07-08T23:08:04Z",
                        "status": "1",
                        },
                    {
                        "id": 77,
                        "created_at": "2021-07-08T23:09:24.948459Z",
                        "last_modified": "2021-07-09T18:55:43.007102Z",
                        "candidate_number": "12d12",
                        "birth_date": "2021-07-27",
                        "first_name": "Serj",
                        "last_name": "Tankian",
                        "test_type": "B",
                        "search_range": "2",
                        "days_to_skip": None,
                        "last_crawled": "2021-07-08T23:09:24Z",
                        "status": "1",
                        },
                    {
                        "id": 78,
                        "created_at": "2021-07-09T18:57:12.463313Z",
                        "last_modified": "2021-07-09T18:57:12.463372Z",
                        "candidate_number": "aaaaaaaaaaa",
                        "birth_date": "2021-07-09",
                        "first_name": "sss",
                        "last_name": "ddd",
                        "test_type": "A",
                        "search_range": "3",
                        "days_to_skip": None,
                        "last_crawled": "2021-07-09T18:56:48Z",
                        "status": "1",
                        }
                    ]
                }
    }


    i = Instructor(data)
    print(i.to_json())


