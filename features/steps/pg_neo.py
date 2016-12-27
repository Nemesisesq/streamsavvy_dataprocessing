from behave import *

from scripts.pg_neo import convert_content_pg_mongoneo

use_step_matcher("re")


@then("we have a list of dictionaries")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    context.result = convert_content_pg_mongoneo()
    pass


@when("we convert all content")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    assert True
    pass