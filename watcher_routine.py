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


def get_instances_to_spawn():
    logger.debug('Fetching instances to spawn')
    data = API.fetch_crawler_instances(role='watch')
    crawlers = data.get('crawlers')
    to_spawn = []

    if crawlers:
        for each in crawlers:
            to_spawn.append(db.CrawlerInstance(each))

    return to_spawn

def spawn_watcher(crawler_instance):
    instructor = crawler_instance.instructor
    proxy = crawler_instance.proxy.get('ip')
    student = crawler_instance.student

    logger.debug("spawning watcher:")
    logger.debug(f"instructor: {instructor.first_name}")
    logger.debug(f"Watcher student: {student.first_name}")

    crawler = Crawler(instructor, proxy)
    
    driver = crawler.get_driver()
    with driver() as driver:
        crawler.setup_page(driver)
        while True:
            if not is_gov_website_working():
                break

            is_instance_active = API.ping_crawler_instance(crawler_instance.id)
            if is_instance_active:
                crawler.update_last_crawled(instructor.id)
                try:
                    crawler.watch(student)
                except Exception as e:
                    error_time = format(datetime.now(), "%d-%m-%Y_%H:%M")
                    #driver.save_screenshot(f'/home/ubuntu/website/static/media/watcher_{error_time}.png')
                    raise e
            else:
                break

            time.sleep(WATCHER_INTERVAL)


if __name__ == "__main__":
    while True:
        if not is_gov_website_working():
            time.sleep(600)
            continue

        to_spawn = get_instances_to_spawn()

        for each in to_spawn:
            p = mp.Process(target=spawn_watcher, args=((each, )))
            p.start()

        if not to_spawn:
            logger.debug("No instances to spawn")

        time.sleep(WATCHER_SPAWN_INTERVAL)
        #time.sleep(600)
        #print(instructor)


    #crawler.scrape()
