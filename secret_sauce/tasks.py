import json
import threading
from functools import partial
from multiprocessing.pool import ThreadPool

import itertools

import logging
from time import sleep

import pika
from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task

from data_processor.shortcuts import debounce
from secret_sauce.autoscale import scale, scale_down
from secret_sauce.tf_idf import ContentEngine
from streamsavvy_dataprocessing.settings import get_env_variable

logger = logging.getLogger('cutthecord')
def runner(func):
    return func()


def get_recomendations(the_json):
    from secret_sauce.tf_idf import ContentEngine

    c_e = ContentEngine()

    p_g = partial(c_e.predict, 'genres', the_json, 10)
    p_t = partial(c_e.predict, 'tags', the_json, 10)
    p_c = partial(c_e.predict, 'cast', the_json, 10)

    x = [p_g, p_t, p_c]

    pool = ThreadPool(3)
    res = pool.map(runner, x)
    pool.close()
    pool.join()

    chain = itertools.chain.from_iterable(res)

    flat = list(chain)

    return flat


def convert_ids(id, suggestion_id_list):
    from data_processor.models import Content
    show = Content.objects.get(guidebox_data__id=id)

    show_list = [Content.objects.get(guidebox_data__id=int(x[0].decode("utf-8"))) for x in suggestion_id_list]

    return show_list


def callback(ch, method, properties, body):
    the_json = json.loads(body.decode('utf-8'))
    from data_processor.models import Content
    c = Content.objects.get(guidebox_data__id=the_json)
    publish_recomendations(c)


rmq_tx_url = get_env_variable('RABBITMQ_BIGWIG_TX_URL')

tx_url_params = pika.URLParameters(rmq_tx_url)
count = 0
def publish_recomendations(p):
    from data_processor.serializers import SuggestionSerializer
    payload = SuggestionSerializer(p).data
    payload = json.dumps(payload)
    connection = pika.BlockingConnection(tx_url_params)
    channel = connection.channel()

    if p:
        channel.queue_declare(queue='reco_engine_results')
        logger.info('sending result for {}'.format(p))

        channel.basic_publish(exchange='',
                              routing_key='reco_engine_results',
                              body=payload)
        # connection.close()


@periodic_task(serializer='json', run_every=(crontab(hour="*", minute="*/10")), name='listen to messenger for id', ignore_result=True)
def listen_to_messenger_for_id():
    rmq_rx_url = get_env_variable('RABBITMQ_BIGWIG_RX_URL')

    url_params = pika.URLParameters(rmq_rx_url)

    connection = pika.BlockingConnection(url_params)

    channel = connection.channel()

    channel.queue_declare(queue='reco_engine')

    channel.basic_consume(callback, queue='reco_engine', no_ack=True)

    if not channel.is_open:
        print("I feel like I want to be around you")
        mq_recieve_thread = threading.Thread(target=channel.start_consuming)
        mq_recieve_thread.start()
        print("when the sun goes down")


@periodic_task(serializer='json', run_every=(crontab(minute="0", hour="0", day_of_week="*")), name='train_content_engine', ignore_result=True)
def train():
    # scale(1, "web" "standard-1X")
    # scale(1, "celery" "standard-2X")
    c_e = ContentEngine()
    c_e.train()
    logger.info("I'm training the recomendation engine")
    sleep (120)
    # scale(0, "hobby")
    # scale_down("web")
    # scale_down("celery")

@shared_task
def train_async():
    train()

def check_for_training_on_startup():

    c_e = ContentEngine()
    keys = c_e.r.keys("ss_reco:*")
    if len(keys) == 0:
        train()
        logger.info("performing initial training of database")

@periodic_task(serializer='json', run_every=(crontab(hour="0", minute="0", day_of_week="*")), name='helloworld', ignore_result=True)
def get_tv_schedules():

    print('Hello world')
#
