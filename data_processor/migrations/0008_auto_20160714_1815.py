# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 18:15
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0007_viewingservices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewingservices',
            name='windows',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]