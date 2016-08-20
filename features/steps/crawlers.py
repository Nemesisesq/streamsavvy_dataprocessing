from behave import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from college_football_scraper.spiders.college_football_spider import CollegeFootballSpider
from data_processor.models import Schedule

use_step_matcher("re")


@when("we run the ncaaf crawler")
def step_impl(context):
    process = CrawlerProcess(get_project_settings())
    process.crawl(CollegeFootballSpider)
    process.start()
    pass


@then("we get schedules with shows")
def step_impl(context):
    assert Schedule.objects.all().count() > 0
    pass
