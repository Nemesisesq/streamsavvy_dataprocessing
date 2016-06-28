# __author__ = 'Nem'
# import os
# from behave import *
#
# @given(u'a value of local')
# def set_local(context):
#     context.local = 'local'
#
# @when(u'we grab ENV_TEST')
# def get_ENV_TEST(context):
#     x = os.environ.get('ENV_TEST')
#     y = os.environ.get('GRAILS_HOME')
#     z = os.environ.get('PATH')
#     context.env_var = os.environ.get('ENV_TEST')
#
# @then(u'ENV_TEST equals local')
# def test_equality(context):
#     assert context.local == context.env_var
