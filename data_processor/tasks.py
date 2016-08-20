import requests
import scrapy
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime, time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from college_football_scraper.spiders.college_football_spider import CollegeFootballSpider
from college_football_scraper.spiders.example import ExampleSpider

logger = get_task_logger(__name__)

def scraper_example(a, b):
    return a + b

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(serializer='json', run_every=(crontab(hour="*", minute="*", day_of_week="*")), name='helloworld', ignore_result=True)
def scraper_runner():
    # print('hello world')
    # r = requests.get('http://localhost:8081')

    # print(r.text )

    logger.info("Start task")
    now = datetime.now()
    result = scraper_example(now.day, now.minute)
    logger.info("Task finished: result = %i" % result)


process = CrawlerProcess(get_project_settings())

@periodic_task(serializer='json', run_every=(crontab( day_of_week="2,3,4")), name=' college football scraper', ignore_results=True)
def example_scraper_test():
    print('college football scraper is runninh' + time.strftime("%c"))
    process.crawl(CollegeFootballSpider)
    process.start()

    return


def example_scraper_test():
    print('')
