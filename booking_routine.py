import sys
import os
import time
import multiprocessing as mp
import mixins
from config import logger
from models import db
from pprint import pprint
from crawler import Crawler


API = mixins.APIMixin()

def get_booking_information():
    data = API.fetch_next_student()

    if data:
        instructor = db.Instructor(data['instructor'])
        student = db.Student(data['student'])

        return (instructor, student)
    else:
        return None

"""
Every 10 minutes make a request to the server asking if there are any
instructors that should be spawned.
"""
def spawn_crawler(instructor, proxy):
    print("spawning crawler:")
    print("instructor: ", instructor.first_name)
    crawler = Crawler(instructor, proxy)
    
    driver = crawler.get_driver()
    with driver() as driver:
        crawler.setup_page(driver)
        while True:
            student = get_student(instructor.id)
            if student:
                print("crawling student: ", student.first_name)
                crawler.scrape(student)
            else:
                print("no student")

            time.sleep(10)




#data = get_instructor()
#if data:
    #instructor, proxy = get_instructor()
    #spawn_crawler(instructor, proxy)

if __name__ == "__main__":
    while True:
        booking_info = get_booking_information()
        if booking_info:
            instructor, student = booking_info
            #TODO
            
            p = mp.Process(target=spawn_crawler, args=(instructor, proxy))
            p.start()

                #spawn_crawler(instructor)
            else:
                print("no instructor")

            #break
        time.sleep(30)
        #print(instructor)


    #crawler.scrape()
