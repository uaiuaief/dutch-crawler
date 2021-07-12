import api_integration as API


r = API.fetch_next_crawl(1)

try:
    r.raise_for_status()
    data = r.json()
    s = Student(data)
    print(s.to_json())
except Exception as e:
    print('no students avaiable')





