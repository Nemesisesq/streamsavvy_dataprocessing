import django


import csv

from popularity.tasks import update_content_popularity

django.setup()





def run():
    update_content_popularity()

