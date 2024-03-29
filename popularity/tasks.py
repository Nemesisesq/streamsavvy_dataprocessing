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
from data_processor.shortcuts import try_catch, debounce, singleton
from streamsavvy_dataprocessing.settings import get_env_variable

logger = logging.getLogger('cutthecord')


# def update_content_popularity():
#     c = Content.objects.all()z
#
#     for i in c:
#         get_popularity_score(i)

@singleton
class PopularityService:
    def get_popularity_score(self, i):
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

    def set_popularity_score(self,json):
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

    def callback(self, ch, method, properties, body):
        the_json = json.loads(body.decode('utf-8'))
        self.set_popularity_score(the_json)

    def listen_to_messenger_for_popularity(self):

        rmq_url = get_env_variable('RABBITMQ_URL')

        print("\n redis_url {} \n".format(rmq_url))
        url_params = pika.URLParameters(rmq_url)

        connection = pika.BlockingConnection(url_params)

        channel = connection.channel()

        channel.queue_declare(queue='popularity')

        channel.basic_consume(self.callback, queue='popularity', no_ack=True)

        print("lay down the threat is real")
        mq_recieve_thread = threading.Thread(target=channel.start_consuming)
        mq_recieve_thread.start()
        print("with his sight goes red again")

        cache.set('yeah_baby', "Naw")

@periodic_task(serializer='json', run_every=(crontab(hour="*", minute="*/10")), name='b', ignore_result=True)
def edd():
    PopularityService().listen_to_messenger_for_popularity()
