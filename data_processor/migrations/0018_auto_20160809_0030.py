# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 00:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0017_auto_20160808_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 9, 0, 30, 23, 956117, tzinfo=utc)),
        ),
    ]
