from behave import *

from data_processor.match_schedules import add_ncaaf_schedules
from data_processor.models import Sport

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
