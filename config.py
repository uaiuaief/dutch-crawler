import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()


#LOGGER
logger = logging.getLogger('crawler')
logging.basicConfig(filename='var/log/crawler.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG, filemode='w')
logger.addHandler(logging.StreamHandler())


#ENV VARIABLES
TWOCAPTCHA_API_KEY = os.environ.get('TWOCAPTCHA_API_KEY')

CRAWLER_USERNAME = os.environ.get('CRAWLER_USERNAME')
CRAWLER_PASSWORD = os.environ.get('CRAWLER_PASSWORD')

WATCHER_INTERVAL = int(os.environ.get('WATCHER_INTERVAL'))

BOOKER_SPAWN_INTERVAL = int(os.environ.get('BOOKER_SPAWN_INTERVAL'))
WATCHER_SPAWN_INTERVAL = int(os.environ.get('WATCHER_SPAWN_INTERVAL'))
