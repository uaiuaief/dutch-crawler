import sys
import os
import time
import multiprocessing as mp


manager = mp.Manager()
instructors = manager.dict()

instructors[1] = False
instructors[2] = False
instructors[3] = False


def f(instructors, crawled_instructor):
    print('starting :', crawled_instructor)
    instructors[crawled_instructor] = True
    #try:
    for i in range(5):
        time.sleep(1)
        print('crawling ', crawled_instructor)
        #raise Exception('timed exc')
    #finally:
    print('stopping :', crawled_instructor)
    instructors[i] = False


if __name__ == "__main__":
    while True:
        i_copy = dict(instructors)
        print(i_copy)
        for each in i_copy:
            print(each)
        #for each in i_copy:
        #    time.sleep(1)
        #    if instructors[each] == False:
        #        p = mp.Process(target=f, args=(instructors, each))
        #        p.start()


