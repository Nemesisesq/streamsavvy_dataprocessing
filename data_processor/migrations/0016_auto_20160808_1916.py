# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 19:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0015_auto_20160808_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 8, 19, 16, 24, 820783, tzinfo=utc)),
        ),
    ]
