from behave import *

from data_processor.match_schedules import add_ncaaf_schedules
from data_processor.models import Sport
from scripts.add_nfl import run

use_step_matcher("re")


@given("a list of ncaaf teams")
def step_impl(context):
    context.teams = Sport.objects.filter(category='College Football')


@when("we match all the schedules")
def step_impl(context):
    add_ncaaf_schedules()


@then("the teams in the Sport model have schedules")
def step_impl(context):
    with open('teams_missing_schedules.txt', 'w') as file:
        for x in context.teams:
            try:
                print(x.schedules.all())
                if x.schedules.all().count() == 0:
                    file.write('\n' + x.title + ' does not have a schedule')
            except:
                file.write('\n' + x.title + ' does not have a schedule set')


        file.close()


@when("we run the nfl script")
def step_impl(context):

    run()


@then("we have teams")
def step_impl(context):
    s = Sport.objects.filter(category='NFL').count()

    assert s > 0
    pass
