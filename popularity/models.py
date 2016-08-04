from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from data_processor.models import Content


class Popularity(models.Model):
    score = models.FloatField(default=0.1)
    date_created = models.DateField(default=datetime.now())
    content = models.ForeignKey(Content)

    class Meta:
        get_latest_by = 'date_created'


