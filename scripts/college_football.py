import django


import csv

from data_processor.match_schedules import add_ncaaf_schedules

django.setup()


from data_processor.models import ServiceDescription


def run():
    add_ncaaf_schedules()
