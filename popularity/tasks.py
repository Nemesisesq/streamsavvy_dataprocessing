import codecs
import json
import logging
import threading

import datetime
import pika
import requests
from celery.schedules import crontab
from celery.task import periodic_task
from django.core.cache import cache
from data_processor.shortcuts import try_catch, debounce
from streamsavvy_dataprocessing.settings import get_env_variable

logger = logging.getLogger('cutthecord')


# def update_content_popularity():
#     c = Content.objects.all()z
#
#     for i in c:
#         get_popularity_score(i)


@try_catch
def get_popularity_score(i):
    query_url = "{popularity_service}".format(popularity_service=get_env_variable('POPULARITY_SERVICE'))
    headers = {'Content-Type': 'application/json'}
    req_data = {"name": i.title}
    res = requests.post(query_url, json.dumps(req_data), headers)
    res_data = res.json()
    if res_data['popularity']:
        from popularity.models import Popularity
        p = Popularity.objects.create(score=res_data['popularity'], content=i)
        p.save()
        i.save()

    logger.info("popularity for {} saved".format(i.title))

@try_catch
def set_popularity_score(json):
    from data_processor.models import Content
    from popularity.models import Popularity

    c = Content.objects.filter(title__iexact=json["name"])

    if c:
        for i in c:

            p = Popularity.objects.create(score=json['popularity'], content=i)
            from popularity.models import TMDB
            t = TMDB.objects.get_or_create(content=i)
            t[0].data = json

            t[0].save()
            p.save()
    logger.info("Added Popularity to {}".format(c))




def callback(ch, method, properties, body):
    the_json = json.loads(body.decode('utf-8'))
    set_popularity_score(the_json)

@debounce(2)
def listen_to_messenger_for_popularity():
    rmq_url = get_env_variable('RABBITMQ_BIGWIG_RX_URL')

    url_params = pika.URLParameters(rmq_url)


    connection = pika.BlockingConnection(url_params)

    channel = connection.channel()

    channel.queue_declare(queue='popularity')

    channel.basic_consume(callback, queue='popularity', no_ack=True)

    yb = cache.get("yeah_baby")
    if not yb:
        print("lay down the threat is real")
        mq_recieve_thread = threading.Thread(target=channel.start_consuming)
        mq_recieve_thread.start()
        print("with his sight goes red again")

        cache.set('yeah_baby', "Naw")

