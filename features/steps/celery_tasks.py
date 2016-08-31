from behave import *

from guide.tasks import get_tv_schedules

use_step_matcher("re")


@then("we have a good time")
def step_impl(context):
    get_tv_schedules()
    """
    :type context: behave.runner.Context
    """
    pass


@when("we call the get schedule task")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass
