# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 15:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0018_auto_20160809_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 9, 15, 28, 19, 58968, tzinfo=utc)),
        ),
    ]
