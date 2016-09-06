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
from guide.models import PostalCode, RoviListings
from guide.views import RoviAPI

logger = get_task_logger(__name__)

def scraper_example(a, b):
    return a + b

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(serializer='json', run_every=(crontab(hour="*", minute="*", day_of_week="*")), name='helloworld', ignore_result=True)
def get_tv_schedules():

    service_listings = RoviListings.objects.all()

    for i in service_listings:
        RoviAPI.get_grid_schedule_for_service_id(i)
