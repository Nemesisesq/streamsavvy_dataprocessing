import csv

from data_processor.models import ServiceDescription


def run ():
    # name =price= description =google_play_link =ios_appstore_link =subscription_link =tooltip_title_link=slug = ""
    r = csv.DictReader(open('serv_desc.csv'))
    x = [i for i in r]

    for d in x:
        locals().update(d)
        v = ServiceDescription()
        v.name = name
        v.price = price
        v.description = description
        v.google_play_link = google_play_link
        v.ios_appstore_link = ios_appstore_link
        v.subscription_link = subscription_link
        v.tooltip_tile_link = tooltip_title_link
        v.slug = slug
        v.save()