from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streamsavvy_dataprocessing.settings')

from django.conf import settings


app = Celery('streamsavvy_dataprocessing')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.control.purge()

app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
