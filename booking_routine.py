import sys
import os
import time
import multiprocessing as mp
import mixins
from datetime import datetime, timezone, timedelta
from config import logger, BOOKER_SPAWN_INTERVAL
from models import db
from pprint import pprint
from crawler import Crawler


API = mixins.APIMixin()

def is_gov_website_working():
    timezone_offset = 2.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    current_time = datetime.now(tzinfo)

    start = datetime.strptime("06:30+0200", "%H:%M%z")
    end = datetime.strptime("23:59+0200", "%H:%M%z")

    #print(f"{current_time.time()} > {start.time()} {current_time.time() > start.time()}")
    #print(f"{current_time.time()} < {end.time()} {current_time.time() < end.time()}")

    if not start.time() < current_time.time() < end.time():
        return False
    else:
        return True

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
    logger.info("Instructor: %s", instructor.first_name)
    logger.info(f"Student: {student.first_name} {student.last_name}")
    crawler = Crawler(instructor, proxy)
    
    driver = crawler.get_driver()
    with driver() as driver:
        crawler.setup_page(driver)
        try:
            crawler.book(student)
        except Exception as e:
            error_time = format(datetime.now(), "%d-%m-%Y_%H:%M")
            driver.save_screenshot(f'/home/ubuntu/website/static/media/booker_{error_time}.png')
            raise e


if __name__ == "__main__":
    while True:
        if not is_gov_website_working():
            time.sleep(600)
            continue
        booking_info = get_booking_information()
        if booking_info:
            instructor, student, proxy = booking_info
            
            p = mp.Process(target=spawn_booker, args=(instructor, student, proxy))
            p.start()
        else:
            logger.debug("No students to book")

        time.sleep(BOOKER_SPAWN_INTERVAL)
