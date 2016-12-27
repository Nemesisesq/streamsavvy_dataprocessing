import itertools
import json
import logging
import threading
from functools import partial
from multiprocessing.pool import ThreadPool

import pika
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from data_processor.shortcuts import singleton, try_catch
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


@try_catch
def g(i):
    from server.models import Content
    return Content.objects.get(guidebox_data__id=int(i))


@singleton
class RecomendationService:
    def on_request(self, ch, method, props, body):
        logger.info("Show Id's recieved for processing")

        the_json = json.loads(body.decode('utf-8'))
        pool = ThreadPool(10)
        p = pool.map(g, the_json)

        pool.close()
        pool.join()

        # for x in p:
        from data_processor.serializers import SuggestionSerializer
        payload = SuggestionSerializer(p, many=True).data
        payload = json.dumps(payload)

        logger.info("{} published to {}# {}".format("Show", props.reply_to, props.correlation_id))
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=payload)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    def listen_to_messenger_for_id(self):
        url = get_env_variable('RABBITMQ_URL')

        url_params = pika.URLParameters(url)

        connection = pika.BlockingConnection(url_params)

        channel = connection.channel()
        logger.info("declaring channel")
        channel.queue_declare(queue='reco_rpc_queue')
        logger.info("defining queue")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.on_request, queue='reco_rpc_queue')

        mq_recieve_thread = threading.Thread(target=channel.start_consuming)
        mq_recieve_thread.start()
        logger.info("Recomendation RPC listening")

@periodic_task(serializer='json', run_every=(crontab(minute="0", hour="0", day_of_week="*")), name='a',
               ignore_result=True)
def train():
    # scale(1, "web" "standard-1X")
    # scale(1, "celery" "standard-2X")
    c_e = ContentEngine()
    c_e.train()
    # logger.info("I'm training the recomendation engine")
    # sleep (120)
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
        logger.info("performing initial training of database")
        train()

#
