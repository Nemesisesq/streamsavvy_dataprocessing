import django


import csv
django.setup()


from data_processor.models import ServiceDescription


def run():
    r = csv.DictReader(open('serv_desc.csv'))
    x = [i for i in r]

    for d in x:

        v = ServiceDescription()
        v.name = d['name']
        v.price = 0.00
        v.description = d['description']
        v.google_play_link = d['google_play_link']
        v.ios_appstore_link = d['ios_appstore_link']
        v.subscription_link = d['subscription_link']
        v.tooltip_tile_link = d['tooltip_tile_link']
        v.slug = d['slug']
        v.save()
