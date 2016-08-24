import json
import urllib
from multiprocessing.dummy import Pool

import re
import requests
from django.core.cache import cache
from fuzzywuzzy import fuzz
from rest_framework.response import Response
from rest_framework.views import APIView

from guide.models import RoviListings, RoviGridSchedule, RoviProgramImages
from guide.serializers import RoviGridScheduleSerializers
from data_processor.constants import sling_channels
from data_processor.shortcuts import lazy_thunkify


class RoviAPI(object):
    api_key = 'p3nh3333exq3umj9ka8uqhee'
    BASE_URL = 'http://api.rovicorp.com/TVlistings/v9/listings/'

    @classmethod
    def get_images_url(cls, program_id):
        program_detail_url = "{}programdetails/{}/info?".format(cls.BASE_URL, program_id)
        params = {'local': 'en-US',
                  'copytextformat': 'PlainText',
                  'include': 'Image',
                  'imagecount': 10,
                  'duration': 20160,
                  'format': 'json',
                  'apikey': cls.api_key,
                  }

        url = program_detail_url + urllib.parse.urlencode(params)

        return url

    @classmethod
    def get_listings_for_zip_code(cls, zip):

        listing_url = "{}services/postalcode/{}/info?".format(cls.BASE_URL, zip)
        params = {'locale': 'en-US', 'countrycode': 'US', 'format': 'json', 'apikey': cls.api_key}

        url = listing_url + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False

    @classmethod
    def retrieve_schedule_from_db(cls, zipcode):
        return RoviGridSchedule.objects.filter(postal_code=zipcode).order_by("-date_added")[:2]

    @classmethod
    def get_schedule_from_rovi_api(cls, service_id):

        listing_url = "{}gridschedule/{}/info?".format(cls.BASE_URL, service_id)
        params = {'locale': 'en-US', 'duration': 60, 'includechannelimages': 'true', 'format': 'json',
                  'apikey': cls.api_key}

        url = listing_url + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False

    @classmethod
    def save_listing(cls, zip, x):
        r = RoviListings.objects.get_or_create(service_id=x['ServiceId'], postal_code=zip, locale='en-US', country='US',
                                               data=x)

        return r[0]

    @classmethod
    def retrive_listing(cls, zip):
        return RoviListings.objects.filter(postal_code=zip)

    @classmethod
    def save_channel_grid(cls, zip, grid):

        g = RoviGridSchedule(
            listing=RoviListings.objects.get(service_id=str(grid['GridScheduleResult']['ServiceId']), postal_code=zip),
            locale='en-US', data=grid, postal_code=zip)
        return g[0]

    @classmethod
    def refresh_grid_schedule(cls, i, zip):
        sched = cls.get_schedule_from_rovi_api(i)

        cls.save_channel_grid(zip, sched)

        pass


@lazy_thunkify
def filter_sling_channels(chan):
    for i in sling_channels:
        z = chan['CallLetters']
        if fuzz.token_set_ratio(chan['SourceLongName'], i) > 95 and not re.search("HD", chan['CallLetters']):
            return True
    return False


class RoviChannelGridView(APIView):
    def get(self, request, zip, format=None):

        show_grids = RoviAPI.retrieve_schedule_from_db(zip)

        if not show_grids:

            service_listings = RoviListings.objects.filter(postal_code=zip)

            if not service_listings:
                service_listings = self.process_new_listings(service_listings, zip)

            grid_list = self.process_new_grid_listing(service_listings)

            show_grids = [RoviAPI.save_channel_grid(zip, grid) for grid in grid_list]

        serializer = RoviGridScheduleSerializers(show_grids, many=True)

        cache.set(zip, serializer.data, timeout=600)

        return Response(serializer.data)

    def process_new_grid_listing(self, service_listings):
        # broadcast_services = [x for x in service_listings if x.data['Type'] == 'Broadcast'][0]
        satellite_services = [x for x in service_listings if x.data['SystemName'] == 'Dish Network'][0]
        # broadcast_grid_response = RoviAPI.get_schedule_from_rovi_api(broadcast_services)
        satellite_grid_response = RoviAPI.get_schedule_from_rovi_api(satellite_services)
        # broadcast_grid_list = json.loads(broadcast_grid_response)
        satellite_grid_list = json.loads(satellite_grid_response)
        satellite_grid_list['GridScheduleResult']['GridChannels'] = [chan for chan in
                                                                     satellite_grid_list['GridScheduleResult'][
                                                                         'GridChannels'] if
                                                                     filter_sling_channels(chan)()]
        grid_list = [satellite_grid_list]

        return grid_list

    def process_new_listings(self, service_listings, zip):
        s = RoviAPI.get_listings_for_zip_code(zip)
        s = json.loads(s)['ServicesResult']['Services']['Service']
        service_listings = [RoviAPI.save_listing(zip, x) for x in s if x.data['SystemName'] == 'Dish Network']
        return service_listings
