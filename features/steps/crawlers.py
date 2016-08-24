from behave import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from college_football_scraper.spiders.college_football_spider import CollegeFootballSpider
from college_football_scraper.spiders.pro_football_spider import ProFootballSpider
from data_processor.models import Schedule, Sport

use_step_matcher("re")


@when("we run the ncaaf crawler")
def step_impl(context):
    process = CrawlerProcess(get_project_settings())
    process.crawl(CollegeFootballSpider)
    process.start()


@then("we get schedules with shows")
def step_impl(context):
    assert Schedule.objects.all().count() > 0


@when("we run the nfl crawler")
def step_impl(context):
    context.teams = Sport.objects.filter(category='NFL')

    process = CrawlerProcess(get_project_settings())
    process.crawl(ProFootballSpider)
    process.start()


@then("we get schedules with nfl games")
def step_impl(context):
    with open('nfl_teams_missing_schedules.txt', 'w') as file:
        for x in context.teams:
            try:
                print(x.schedules.all())
                if x.schedules.all().count() == 0:
                    file.write('\n' + x.title + ' does not have a schedule')
            except:
                file.write('\n' + x.title + ' does not have a schedule set')

        file.close()
    assert Schedule.objects.filter(team__category='NFL')
