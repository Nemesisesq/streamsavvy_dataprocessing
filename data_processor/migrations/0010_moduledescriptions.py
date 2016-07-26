# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 20:36
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0009_auto_20160714_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleDescriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.TextField(blank=True, null=True)),
                ('service', models.TextField(blank=True, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.TextField(blank=True, null=True)),
                ('networks', jsonfield.fields.JSONField(blank=True, null=True)),
                ('category', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
