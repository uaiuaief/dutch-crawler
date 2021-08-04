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

        self.test_type = profile['test_type']
        self.first_name = profile['full_name']
        self.driving_school_name = profile['driving_school_name']
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
        if value:
            self._date_to_book = DateFound(value)
        else:
            self._date_to_book = None

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
        self.test_center_name = data.get('test_center_name')
        self.test_center = data.get('test_center')
        self.date = data['date']
        self.test_type = data['test_type']
        self.week_day = data['week_day']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.free_slots = data['free_slots']
        self.user_id = data['found_by']

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = datetime.strptime(value, "%Y-%m-%d").date()

    @property
    def test_center(self):
        return self._test_center

    @test_center.setter
    def test_center(self, test_center):
        if test_center:
            self._test_center = TestCenter(test_center)
        else:
            self._test_center = None



if __name__ == "__main__":
    data = {
            "id": 1,
            "email": "john@john.com",
            "profile": {
                "first_name": "Abraham",
                "last_name": "Lincoln",
                "mobile_number": "123123123113",
                "driving_school_name": "Suja driving school",
                "test_type": "A",
                "gov_username": "Kirmit91",
                "gov_password": "Rijswijk123!",
                "student_limit": 100,
                "status": "2",
                "test_center": {
                    "id": 94,
                    "created_at": "2021-07-09T17:42:37.503458Z",
                    "last_modified": "2021-07-09T17:42:37.503505Z",
                    "name": "Rijswijk Zh (Lange Kleiweg 30)"
                    },
                "students": [
                    {
                        "id": 10,
                        "date_to_book": {
                            "id": 30,
                            "date": "2021-08-05",
                            "week_day": "1",
                            "start_time": "22:50:00",
                            "end_time": "23:30:00",
                            "free_slots": 3,
                            "test_type": "A",
                            "test_center": {
                                "id": 94,
                                "created_at": "2021-07-09T17:42:37.503458Z",
                                "last_modified": "2021-07-09T17:42:37.503505Z",
                                "name": "Rijswijk Zh (Lange Kleiweg 30)"
                                },
                            "found_by": 1
                            },
                        "created_at": "2021-07-29T18:34:05.587507Z",
                        "last_modified": "2021-07-31T18:09:27.825748Z",
                        "candidate_number": "4533466125",
                        "birth_date": "2021-07-29",
                        "first_name": "Abou",
                        "last_name": "Omar",
                        "search_range": "2",
                        "test_booked": False,
                        "days_to_skip": "4",
                        "status": "3"
                        }
                    ]
                }
            }


    i = Instructor(data)
    print(i.to_json())


