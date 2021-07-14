import sys
import os
import time
import mixins
from config import logger
from models import db
from pprint import pprint
from crawler import Crawler


API = mixins.APIMixin()

def get_instructor():
    data = API.fetch_instructor_to_crawl()

    if data:
        return db.Instructor(data)
    else:
        return None

def get_student(user_id):
    data = API.fetch_next_student(user_id)

    if data:
        return db.Student(data)
    else:
        return None


"""
Every 10 minutes make a request to the server asking if there are any
instructors that should be spawned.
"""
#while True:
#    instructor = get_instructor()
#    print(instructor.to_json())
#    break


instructor = get_instructor()
if instructor:
    crawler = Crawler(instructor)
    crawler.setup_page()
    student = get_student(instructor.id)
    #crawler.scrape(student)

    #while True:
        #student = get_student(instructor.id)
        #crawler.scrape(student)

#print(instructor)


#crawler.scrape()
