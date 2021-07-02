import json


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


class Instructor(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        profile = data['profile']

        self.first_name = profile['first_name']
        self.last_name = profile['last_name']
        self.gov_username = profile['gov_username']
        self.gov_password = profile['gov_password']
        self.students = profile['students']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
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
        self.earliest_test_date = data['earliest_test_date']
        self.test_centers = data['test_centers']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def test_centers(self):
        return self._test_centers

    @test_centers.setter
    def test_centers(self, test_centers):
        arr = [TestCenter(each) for each in test_centers]

        self._test_centers = arr


class TestCenter(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


if __name__ == "__main__":
    data = {
            "id": 1,
            "email": "john@john.com",
            "profile": {
                "first_name": "Test",
                "last_name": "Instructor",
                "mobile_number": "999999999999999",
                "gov_username": "Kirmit91",
                "gov_password": "Rijswijk123!",
                "students": [
                    {
                        "id": 1,
                        "created_at": "2021-07-02T00:31:57.887821Z",
                        "last_modified": "2021-07-02T00:31:57.887885Z",
                        "candidate_number": "4545179630",
                        "birth_date": "1994-12-27",
                        "first_name": "Test",
                        "last_name": "Student",
                        "test_type": "B-H",
                        "earliest_test_date": "2021-07-02",
                        "days_to_skip": "15,16",
                        "last_crawled": "2021-07-02T00:30:42Z",
                        "info_validation": "unchecked",
                        "test_centers": [
                            {
                                "id": 1,
                                "created_at": "2021-07-02T00:31:32.249116Z",
                                "last_modified": "2021-07-02T00:31:32.249169Z",
                                "name": "Amsterdam (Naritaweg 150)"
                                },
                            {
                                "id": 2,
                                "created_at": "2021-07-02T00:31:40.150639Z",
                                "last_modified": "2021-07-02T00:31:40.150707Z",
                                "name": "Almelo (Bedrijvenpark Twente 305)"
                                },
                            {
                                "id": 3,
                                "created_at": "2021-07-02T00:31:48.599391Z",
                                "last_modified": "2021-07-02T00:31:48.599547Z",
                                "name": "Kerkrade (Spekhofstraat 24)"
                                }
                            ]
                        },
                    {
                        "id": 2,
                        "created_at": "2021-07-02T16:46:57.121123Z",
                        "last_modified": "2021-07-02T16:46:57.121827Z",
                        "candidate_number": "9999999999999",
                        "birth_date": "2021-07-02",
                        "first_name": "invalid",
                        "last_name": "student",
                        "test_type": "A",
                        "earliest_test_date": "2021-07-02",
                        "days_to_skip": "1",
                        "last_crawled": "2021-07-02T16:46:32Z",
                        "info_validation": "unchecked",
                        "test_centers": [
                            {
                                "id": 2,
                                "created_at": "2021-07-02T00:31:40.150639Z",
                                "last_modified": "2021-07-02T00:31:40.150707Z",
                                "name": "Almelo (Bedrijvenpark Twente 305)"
                                }
                            ]
                        }
                    ]
                }
            } 

    #c = Instructor(data)
    #print(c.to_json())
