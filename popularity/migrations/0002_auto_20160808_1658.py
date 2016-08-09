# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 16:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('popularity', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='popularity',
            options={'get_latest_by': 'date_created'},
        ),
        migrations.AlterField(
            model_name='popularity',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 8, 16, 58, 50, 166351, tzinfo=utc)),
        ),
    ]