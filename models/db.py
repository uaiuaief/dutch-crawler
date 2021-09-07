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


class CrawlerInstance(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        self.instructor = data['instructor']
        self.student = data['student']
        self.proxy = data['proxy']
        self.role = data['role']
        self.last_ping = data['last_ping']

    @property
    def instructor(self):
        return self._instructor

    @instructor.setter
    def instructor(self, value):
        self._instructor = Instructor(value)

    @property
    def student(self):
        return self._student

    @student.setter
    def student(self, value):
        value['date_to_book'] = None
        self._student = Student(value)


if __name__ == "__main__":
    data = {
            "crawlers": [
                {
                    "id": 1,
                    "instructor": {
                        "id": 45,
                        "email": "bookable@bookable.com",
                        "profile": {
                            "full_name": "Bookable user",
                            "mobile_number": "1231212322",
                            "gov_username": "Rijschool Bezuidenhout",
                            "gov_password": "Bristol1990..",
                            "student_limit": 100,
                            "status": "2",
                            "test_type": "BTH",
                            "driving_school_name": "Bookable",
                            "test_center": {
                                "id": 94,
                                "created_at": "2021-07-09T17:42:37.503458Z",
                                "last_modified": "2021-07-09T17:42:37.503505Z",
                                "name": "Rijswijk Zh (Lange Kleiweg 30)"
                                },
                            "students": [
                                {
                                    "id": 16,
                                    "date_to_book": {
                                        "id": 1520,
                                        "date": "2021-11-26",
                                        "week_day": "1",
                                        "start_time": "12:40:00",
                                        "end_time": "13:10:00",
                                        "free_slots": 2,
                                        "test_type": "BTH",
                                        "test_center": {
                                            "id": 94,
                                            "created_at": "2021-07-09T17:42:37.503458Z",
                                            "last_modified": "2021-07-09T17:42:37.503505Z",
                                            "name": "Rijswijk Zh (Lange Kleiweg 30)"
                                            },
                                        "found_by": 30
                                        },
                                    "created_at": "2021-08-04T20:46:31.677034Z",
                                    "last_modified": "2021-09-04T17:21:09.006305Z",
                                    "candidate_number": "4555410025",
                                    "birth_date": "2021-07-27",
                                    "first_name": "Bookable Student",
                                    "last_name": "Faissal Zefri",
                                    "search_range": "2",
                                    "days_to_skip": None,
                                    "last_crawled": "2021-09-04T17:21:09.006113Z",
                                    "status": "3"
                                    }
                                ],
                            "search_count": 200
                            }
                        },
                        "student": {
                                "id": 16,
                                "created_at": "2021-08-04T20:46:31.677034Z",
                                "last_modified": "2021-09-04T17:21:09.006305Z",
                                "candidate_number": "4555410025",
                                "birth_date": "2021-07-27",
                                "first_name": "Bookable Student",
                                "last_name": "Faissal Zefri",
                                "search_range": "2",
                                "days_to_skip": None,
                                "last_crawled": "2021-09-04T17:21:09.006113Z",
                                "status": "3",
                                "instructor": {
                                    "id": 30,
                                    "created_at": "2021-08-04T20:43:30.328523Z",
                                    "last_modified": "2021-09-07T16:19:00.466204Z",
                                    "driving_school_name": "Bookable",
                                    "full_name": "Bookable user",
                                    "mobile_number": "1231212322",
                                    "gov_username": "Rijschool Bezuidenhout",
                                    "gov_password": "Bristol1990..",
                                    "test_type": "BTH",
                                    "search_count": 200,
                                    "student_limit": 100,
                                    "last_crawled": "2021-08-05T21:17:38Z",
                                    "status": "2",
                                    "user": 45,
                                    "test_center": 94
                                    },
                                "date_to_book": {
                                    "id": 1520,
                                    "created_at": "2021-08-08T21:32:28.460420Z",
                                    "last_modified": "2021-08-08T21:54:06.064056Z",
                                    "date": "2021-11-26",
                                    "week_day": "1",
                                    "status": "2",
                                    "start_time": "12:40:00",
                                    "end_time": "13:10:00",
                                    "free_slots": 2,
                                    "test_type": "BTH",
                                    "test_center": 94,
                                    "found_by": 30
                                    }
                                },
                        "proxy": {
                                "id": 32,
                                "created_at": "2021-07-15T20:33:56.317758Z",
                                "last_modified": "2021-08-05T18:10:35.802115Z",
                                "ip": "163.198.133.250:3128",
                                "use_count": 0,
                                "ban_count": 0,
                                "is_banned": False,
                                "last_used": "2021-08-04T20:58:06.328084Z"
                                },
                        "last_ping": None,
                        "role": "watch"
    }
        ]
        }



    i = CrawlerInstance(data['crawlers'][0])
    #print(i.student.to_json())
    print(i.to_json())


