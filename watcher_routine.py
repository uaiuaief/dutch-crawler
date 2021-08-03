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
            if student:
                print("Watcher student: ", student.first_name)
                crawler.watch(student)

            time.sleep(60)




#data = get_instructor()
#if data:
    #instructor, proxy = get_instructor()
    #spawn_crawler(instructor, proxy)

if __name__ == "__main__":
    while True:
        watcher_info = get_watcher_info()
        if watcher_info:
            instructor, proxy, student = watcher_info
            if instructor:
                p = mp.Process(target=spawn_watcher, args=(instructor, proxy, student))
                p.start()
            else:
                print("no instructor")

            #break
        time.sleep(1000)
        #print(instructor)


    #crawler.scrape()
