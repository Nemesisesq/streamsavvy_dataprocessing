from functools import partial

from behave import *

from data_processor.models import Content
from secret_sauce.tasks import RecomendationService, get_recomendations
from secret_sauce.tf_idf import ContentEngine


use_step_matcher("re")


@given("our content engine")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    context.c_e = ContentEngine()
    pass


@when("we train our content engine")
def step_impl(context):
    context.c_e.train()
    """
    :type context: behave.runner.Context
    """
    pass


@step("We make a prediction")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    predict_genres = partial(context.c_e.predict, 'genres', 134, 10)
    predict_tags = context.c_e.predict('tags', 134, 500)
    predict_cast = context.c_e.predict('cast', 134, 500)

    g = convert_ids(134, predict_genres())
    t = convert_ids(134, predict_tags)
    c = convert_ids(134, predict_cast)

    print("\n", g)
    print("\n", t)
    print("\n", c)

    # g_ids = [int(x[0].decode("utf-8")) for x in predict_genres]
    t_ids = [int(x[0].decode("utf-8")) for x in predict_tags]
    c_ids = [int(x[0].decode("utf-8")) for x in predict_cast]

    # print("\n", g_ids)
    print("\n", t_ids)
    print("\n", c_ids)

    # s1 = set(g_ids).intersection(t_ids)
    # s2 = set(g_ids).intersection(c_ids)
    s3 = set(c_ids).intersection(t_ids)

    # print("\n", s1)
    # print("\n", s2)
    print("\n", s3)

    # print([Content.objects.get(guidebox_data__id=x) for x in s1])
    # print([Content.objects.get(guidebox_data__id=x) for x in s2])
    print([Content.objects.get(guidebox_data__id=x) for x in s3])


    assert (True)


def convert_ids(id, suggestion_id_list):
    show = Content.objects.get(guidebox_data__id=id)

    show_list = [Content.objects.get(guidebox_data__id=int(x[0].decode("utf-8"))) for x in suggestion_id_list]

    return (show, show_list)


@given("an id")
def step_impl(context):
    context.id = 28164
    """
    :type context: behave.runner.Context
    """
    pass


@when("we get_recomendations")
def step_impl(context):
    context.recomendations = get_recomendations(context.id)
    """
    :type context: behave.runner.Context
    """


    pass


@then("we get a combined list of shows")
def step_impl(context):

    assert type(context.recomendations) is list
    """
    :type context: behave.runner.Context
    """
    pass


@given("a payload")
def step_impl(context):

    context.payload = "hello world"
    """
    :type context: behave.runner.Context
    """
    pass


@then("we publish the payload to RabbitMQ")

def step_impl(context):
    RecomendationService().publish_recomendations(context.payload)
    assert True

    """
    :type context: behave.runner.Context
    """
    pass
