from behave import *

use_step_matcher("re")


@given("a package")
def step_impl(context):

    context.package = context.rest_client.get('')
    """
    :type context: behave.runner.Context
    """
    pass

@when("we pull out the chanels")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass




@then("we have a list of channels")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass
