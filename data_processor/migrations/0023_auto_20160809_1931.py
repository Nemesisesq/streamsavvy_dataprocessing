# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 19:31
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0022_auto_20160809_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduledescriptions',
            name='networks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sport',
            name='json_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
        ),
        migrations.AlterField(
            model_name='viewingservices',
            name='windows',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
