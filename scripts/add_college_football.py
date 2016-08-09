import django

import csv

django.setup()

from data_processor.models import Sport
from pymongo import MongoClient


def run():
    client = MongoClient('mongodb://localhost:27017')
    db = client.sports
    collection = db.Y2000

    for team in collection.find():
        print(team)
        team['tag_list'] = [i for i in team['tag_list'] if i != " "]
        team['network_list'] = [i for i in team['network_list'] if i != " "]

        del team['_id']

        v = Sport()
        v.title  = "{} Football".format(team['college_name'])
        v.category = 'College Football'
        v.json_data = team
        v.save()

        print("{} saved!".format(v))
