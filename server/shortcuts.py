import json
import os
from urllib.parse import urlparse

from django.http import HttpResponseNotAllowed
import yaml
import psycopg2

__author__ = 'Nem'


def try_catch(f):
    def handleProblems(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("there was a problem with {} with {} and {}".format(f.__name__, args, kwargs))
            print("-" * 60)

            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=4, file=sys.stdout)
            print("-" * 60)
    return handleProblems


def api_json_post(view_func):
    """
    View decorator, which wraps the request and expects posted Json
    :param view_func:
    :return:
    """

    def wrapped(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])

        the_json = json.loads(str(request.body, encoding='utf-8'))

        return view_func(request, the_json, *args, **kwargs)

    return wrapped


class SettingsVars(object):
    facebook = {}

    def __init__(self, BASE_DIR):
        self.get_facebook(BASE_DIR)

    def get_facebook(self, BASEDIR):
        with open(os.path.join(BASEDIR, 'settings_vars.yaml')) as file_descriptor:
            data = yaml.load(file_descriptor)
            self.facebook = data['facebook']
        return data


class DBurl(object):
    url = ''

    def __init__(self, BASE_DIR):
        self.get_db_url(BASE_DIR)

    def get_db_url(self, BASE_DIR):
        try:

            with open(os.path.join(BASE_DIR, 'db.yaml')) as file:
                self.url = yaml.load(file)['postgres_url']

            result = urlparse(self.url)
            u = result.username
            p = result.password
            d = result.path[1:]
            h = result.hostname
            connection = psycopg2.connect(
                database=d,
                user=u,
                password=p,
                host=h
            )

            return self.url
        except Exception as e:
            self.url = 'sqlite:///db.sqlite3'
            return 'sqlite:///db.sqlite3'


from queue import Queue
from threading import Thread


class asynchronous(object):
    def __init__(self, func):
        self.func = func

        def threaded(*args, **kwargs):
            self.queue.put(self.func(*args, **kwargs))

        self.threaded = threaded

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.queue = Queue()
        thread = Thread(target=self.threaded, args=args, kwargs=kwargs);
        thread.start();
        return asynchronous.Result(self.queue, thread)

    class NotYetDoneException(Exception):
        def __init__(self, message):
            self.message = message

    class Result(object):
        def __init__(self, queue, thread):
            self.queue = queue
            self.thread = thread

        def is_done(self):
            return not self.thread.is_alive()

        def get_result(self):
            if not self.is_done():
                raise asynchronous.NotYetDoneException('the call has not yet completed its task')

            if not hasattr(self, 'result'):
                self.result = self.queue.get()

            return self.result


import threading, sys, functools, traceback


def lazy_thunkify(f):
    """Make a function immediately return a function of no args which, when called,
    waits for the result, which will start being processed in another thread."""

    @functools.wraps(f)
    def lazy_thunked(*args, **kwargs):
        wait_event = threading.Event()

        result = [None]
        exc = [False, None]

        def worker_func():
            try:
                func_result = f(*args, **kwargs)
                result[0] = func_result
            except Exception as e:
                exc[0] = True
                exc[1] = sys.exc_info()
                print("Lazy thunk has thrown an exception (will be raised on thunk()):\n%s" % (
                    traceback.format_exc()))
            finally:
                wait_event.set()

        def thunk():
            wait_event.wait()
            if exc[0]:
                raise Exception(exc[1][0], exc[1][1], exc[1][2])

            return result[0]

        threading.Thread(target=worker_func).start()

        return thunk

    return lazy_thunked


import functools, logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class log_with(object):
    '''Logging decorator that allows you to log with a
specific logger.
'''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering {}'
    EXIT_MESSAGE = 'Exiting {}'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        '''Returns a wrapper that wraps func.
The wrapper will log the entry and exit points of the function
with logging.INFO level.
'''
        # set logger if it was not set earlier
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            self.logger.info(
                self.ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            f_result = func(*args, **kwds)
            self.logger.info(
                self.EXIT_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            return f_result

        return wrapper
