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
    booking_info = None

    if data:
        proxy = API.fetch_valid_proxy()
        if proxy:
            user = db.Instructor(data['user'])
            student = db.Student(data['student'])

            booking_info = (user, student, proxy['ip'])

    return booking_info

def spawn_booker(instructor, student, proxy):
    logger.info("spawning crawler:")
    logger.info(f"Instructor: {instructor.first_name}")
    logger.info(f"Student: {student.first_name} {student.last_name}")
    crawler = Crawler(instructor, proxy)
    
    driver = crawler.get_driver()
    with driver() as driver:
        crawler.setup_page(driver)
        crawler.book(student)


if __name__ == "__main__":
    while True:
        booking_info = get_booking_information()
        if booking_info:
            instructor, student, proxy = booking_info
            
            p = mp.Process(target=spawn_booker, args=(instructor, student, proxy))
            p.start()
        else:
            print("No students to book")

        time.sleep(10)
