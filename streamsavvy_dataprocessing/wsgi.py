"""
WSGI config for streamsavvy_dataprocessing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import logging
from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application

from popularity.tasks import PopularityService
from secret_sauce.tasks import RecomendationService, check_for_training_on_startup

logger = logging.getLogger('cutthecord')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamsavvy_dataprocessing.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)


logger.info("listening for popularity")
p = PopularityService
p.listen_to_messenger_for_popularity()


logger.info("listening for show recomendations")
RecomendationService.listen_to_messenger_for_id()

logger.info("checking if the db is trained on startup")
check_for_training_on_startup()


