import sys
import os
import time
import multiprocessing as mp
import mixins
from datetime import datetime, timezone, timedelta
from config import logger, WATCHER_INTERVAL, WATCHER_SPAWN_INTERVAL
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

def get_watcher_info():
    data = API.fetch_watcher_info()

    if data:
        user = data.get('user')
        student = data.get('student')
        proxy = data.get('proxy')

        return (db.Instructor(user), proxy['ip'], db.Student(student))
    else:
        return None

def spawn_watcher(instructor, proxy, student):
    print("spawning crawler:")
    print("instructor: ", instructor.first_name)
    crawler = Crawler(instructor, proxy)
    
    driver = crawler.get_driver()
    with driver() as driver:
        crawler.setup_page(driver)
        while True:
            if not is_gov_website_working():
                break
            if student:
                print("Watcher student: ", student.first_name)
                crawler.update_last_crawled(instructor.id)
                crawler.watch(student)

            time.sleep(WATCHER_INTERVAL)




if __name__ == "__main__":
    while True:
        if not is_gov_website_working():
            time.sleep(600)
        logger.debug('getting watcher info')
        watcher_info = get_watcher_info()
        if watcher_info:
            instructor, proxy, student = watcher_info
            if instructor:
                p = mp.Process(target=spawn_watcher, args=(instructor, proxy, student))
                p.start()
            else:
                print("no instructor")

            #break
        time.sleep(WATCHER_SPAWN_INTERVAL)
        #print(instructor)


    #crawler.scrape()
