# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0021_auto_20160809_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
