import sys
import os
import time
import multiprocessing as mp
import mixins
from datetime import datetime, timezone, timedelta
from config import logger, BOOKER_SPAWN_INTERVAL, BOOKER_INTERVAL
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

def get_instances_to_spawn():
    logger.debug('Fetching instances to spawn')
    data = API.fetch_crawler_instances(role='book')
    crawlers = data.get('crawlers')
    to_spawn = []

    if crawlers:
        for each in crawlers:
            to_spawn.append(db.CrawlerInstance(each))

    return to_spawn

def get_date_to_book(student_id):
    data = API.get_student_date_to_book(student_id)
    if data:
        return db.DateFound(data)
    else:
        return None

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

def spawn_booker(crawler_instance):
    instructor = crawler_instance.instructor
    proxy = crawler_instance.proxy.get('ip')
    student = crawler_instance.student

    logger.info("Spawning booker:")
    logger.info("Instructor: %s", instructor.first_name)
    logger.info(f"Student: {student.first_name} {student.last_name}")
    crawler = Crawler(instructor, proxy)
    
    driver = crawler.get_driver()
    with driver() as driver:
        crawler.setup_booking_crawler(driver, student)
        while True:
            is_instance_active = API.ping_crawler_instance(crawler_instance.id)
            if is_instance_active:
                try:
                    logger.info("Fetching for dates")
                    date_to_book = get_date_to_book(student.id)
                    if date_to_book:
                        logger.info("Booking date")
                        crawler.book(student, date_to_book)
                        break
                    else:
                        logger.info("No date to book")

                except Exception as e:
                    error_time = format(datetime.now(), "%d-%m-%Y_%H:%M")
                    #driver.save_screenshot(f'/home/ubuntu/website/static/media/booker_{error_time}.png')
                    raise e
            else:
                break

            time.sleep(BOOKER_INTERVAL)


if __name__ == "__main__":
    while True:
        if not is_gov_website_working():
            time.sleep(600)
            continue

        to_spawn = get_instances_to_spawn()

        for each in to_spawn:
            p = mp.Process(target=spawn_booker, args=((each, )))
            p.start()

        if not to_spawn:
            logger.debug("No instances to spawn")

        time.sleep(BOOKER_SPAWN_INTERVAL)
