from behave import *

from data_processor.models import Content
from popularity.tasks import get_popularity_score


@given("a package")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("we pull out the channels")
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


@given("The Content {content}")
def step_impl(context, content):
    context.show = Content.objects.get(title=content)
    context.popularity_length = len(context.show.popularity_set.all())
    assert context.show.title == content

@when("We call the popularity service")
def step_impl(context):
    get_popularity_score(context.show)




@then("Content has a popularity score")
def step_impl(context):
    assert len(context.show.popularity_set.all()) > context.popularity_length

