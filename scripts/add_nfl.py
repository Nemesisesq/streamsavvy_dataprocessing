import django

import csv

django.setup()

from data_processor.models import Sport
from pymongo import MongoClient


def run():
    r = csv.DictReader(open('pro_football_data.csv', encoding='ISO-8859-1'))

    x = [i for i in r]

    for team in x:
        print(team)
        team['tag_list'] = [i for i in team['tag_list'].split(",") if i != " "]
        team['network_list'] = [i for i in team['network_list'].split(",") if i != " "]



        v = Sport()
        v.title  = team['Team']
        v.category = 'NFL'
        v.json_data = team
        v.save()

        print("{} saved!".format(v))
