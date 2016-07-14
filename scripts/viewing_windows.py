import django


import csv
django.setup()


from data_processor.models import ViewingServices


def run():
    r = csv.DictReader(open('vw.csv'))
    x = [i for i in r]

    print(x[0])

    for d in x:

        v = ViewingServices()
        v.name = d['name']
        v.price = d['price']
        if 'or' in d['windows']:
            vwlist = d['windows'].split('or')
        else:
            vwlist = d['windows'].split(',')
        v.windows = vwlist
        v.ppv = d['ppv'] or False
        v.save()
