import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'streamsavvy_dataprocessing.settings'
# os.environ['REDIS_URL'] = 'http://localhost:6379'
# Even though the environment variable is set, this still may be
# necessary. Or may be CYA insurance
import django

django.setup()

from splinter.browser import Browser
from rest_framework.test import APIClient


def before_tag(context, tag):
    if tag == 'rest_api':
        context.rest_client = APIClient()
    if tag == 'browser':
        context.browser = Browser()


def before_all(context):
    #### Take a test runner hostage ###
    from django.test.runner import DiscoverRunner

    context.runner = DiscoverRunner()



def after_tag(context, tag):
    if tag == 'browser':
        context.browser.quit()
        context.browser = None
