# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0025_auto_20160817_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='date_created',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
