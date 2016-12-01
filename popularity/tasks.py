import json
import logging
import urllib

import requests
from celery.schedules import crontab
from celery.task import periodic_task

from data_processor.models import Content
from data_processor.shortcuts import api_json_post, try_catch
from popularity.models import Popularity
from streamsavvy_dataprocessing.settings import get_env_variable

logger = logging.getLogger('cutthecord')


def update_content_popularity():
    c = Content.objects.all()

    for i in c:
        get_popularity_score(i)


@try_catch
def get_popularity_score(i):
    query_url = "{popularity_service}".format(popularity_service=get_env_variable('POPULARITY_SERVICE'))
    headers = {'Content-Type': 'application/json'}
    req_data = {"name": i.title}
    res = requests.post(query_url, json.dumps(req_data), headers)
    res_data = res.json()
    if res_data['popularity']:
        p = Popularity.objects.create(score=res_data['popularity'], content=i)
        p.save()
        i.save()

    logger.info("popularity for {} saved".format(i.title))


@periodic_task(serializer='json', run_every=(crontab()), name='helloworld',
               ignore_result=True)
def hello():
    print("hello world")
