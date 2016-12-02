from datetime import datetime

import django
# from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from jsonfield import JSONField

from data_processor.models import Content


class Popularity(models.Model):
    score = models.FloatField(default=0.1)
    date_created = models.DateTimeField()
    content = models.ForeignKey(Content)

    class Meta:
        get_latest_by = 'date_created'

    def save(self, *args, **kwargs):
        self.content.curr_pop_score = self.score
        self.date_created = datetime.utcnow()
        return super(Popularity, self).save(*args, **kwargs)


class TMDB(models.Model):
    data = JSONField(blank=True, null=True)
    content = models.ForeignKey(Content)
    date_created = models.DateTimeField()

    class Meta:
        get_latest_by = 'date_created'

    def save(self, *args, **kwargs):
        # self.content.curr_pop_score = self.score
        self.date_created = datetime.utcnow()
        return super(TMDB, self).save(*args, **kwargs)

