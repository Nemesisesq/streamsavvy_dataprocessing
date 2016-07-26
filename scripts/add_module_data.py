import json

import django

import csv

django.setup()

from data_processor.models import ModuleDescriptions


def run():
    r = csv.DictReader(open('sports_module_options.csv'))

    x = [i for i in r]

    print(x[0])

    for d in x:
        m = ModuleDescriptions()

        m.level = d['level']
        m.service = d['service']
        m.cost = d['price']
        m.description = d['description']
        m.networks = d['networks']
        m.category = d['category']

        m.save()
