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
from data_processor.shortcuts import lazy_thunkify, try_catch, api_json_post
from streamsavvy_dataprocessing.settings import get_env_variable


class RoviAPI(object):
    api_key = 'rj5pcy96h2uee7gmesf755ay'
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
    @try_catch
    def retrieve_schedule_from_db(cls, zipcode):
        return RoviGridSchedule.objects.filter(postal_code=zipcode).latest('date_added')

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

        g = RoviGridSchedule()

        if type(grid) == str:
            grid = json.loads(grid)

        g.listing = RoviListings.objects.filter(service_id=grid['GridScheduleResult']['ServiceId'])[0]

        g.locale = 'en-US'
        g.data = grid
        g.postal_code = zip

        g.save()

        return g

    @classmethod
    def filter_for_live_services(self, chan):
        headers = {'Content-Type': 'application/json'}
        url = "{base}/{path}".format(base=get_env_variable('NODE_DATA_SERVICE'), path='guide')
        res = requests.post(url, data=json.dumps(chan), headers=headers)
        return res.json()

    result_dict = {}

    @classmethod
    def get_grid_schedule_for_service_id(cls, service_id):
        sched = cls.get_schedule_from_rovi_api(service_id)

        sched = json.loads(sched)

        sched = cls.filter_schedule(sched)

        sched = cls.process_chans_for_streaming(sched)

        cls.save_channel_grid(service_id.postal_code, sched)

        return sched

    @classmethod
    def process_chans_for_streaming(cls, sched):
        truncated_chan = [cls.create_payload_dict(i) for i in sched['GridScheduleResult']['GridChannels']]
        pool = Pool(20)
        results = pool.map(cls.filter_for_live_services, truncated_chan)
        pool.close()
        pool.join()
        for chan in results:
            cls.result_dict[chan['SourceId']] = chan

        # sched['GridScheduleResult']['GridChannels'] = [chan for chan in results]
        new_sched = [cls.match_streaming_services(i) for i in sched['GridScheduleResult']['GridChannels']]
        #
        sched['GridScheduleResult']['GridChannels'] = new_sched

        return sched

    @classmethod
    def filter_schedule(cls, sched):

        filter_list = ['SIRIUS', 'VOD', 'SXM', 'XM']

        filter_chans = [x for x in sched['GridScheduleResult']['GridChannels'] if x['CallLetters'] not in filter_list]

        filter_chans = [x for x in filter_chans if not re.search("(HD)", x['CallLetters'])]

        filter_chans = cls.remove_duplicates(filter_chans)

        sched['GridScheduleResult']['GridChannels'] = filter_chans

        return sched

    @classmethod
    def create_payload_dict(cls, chan):
        return {
            'CallLeters': chan['CallLetters'],
            'DisplayName': chan['DisplayName'],
            'SourceLongName': chan['SourceLongName'],
            'SourceId': chan['SourceId']

        }

    @classmethod
    def remove_duplicates(cls, chans):
        checked_array = []
        new_array = []

        for c in chans:
            if c['CallLetters'] not in checked_array:
                checked_array.append(c['CallLetters'])
                new_array.append(c)

        return new_array

    @classmethod
    def match_streaming_services(cls, i):
        i['streamingServices'] = cls.result_dict[i['SourceId']]['streamingServices']
        return i


def filter_sling_channels(chan):
    for i in sling_channels:
        z = chan['CallLetters']
        x = "HD"
        if fuzz.token_set_ratio(chan['SourceLongName'], i) > 95 and not re.search('HD', chan['CallLetters']):
            return True
    return False


class RoviChannelGridView(APIView):
    def get(self, request, lat, long):

        zip_code = self.get_zip_code_from_coords(lat, long)

        show_grids = RoviAPI.retrieve_schedule_from_db(zip_code)

        if not show_grids:

            service_listings = RoviListings.objects.filter(postal_code=zip_code)

            if not service_listings:
                service_listings = self.process_new_listings(service_listings, zip_code)

            grid_list = self.process_new_grid_listing(service_listings)

            show_grids = [RoviAPI.save_channel_grid(zip_code, grid) for grid in grid_list]

        else:
            show_grids = [show_grids]

        serializer = RoviGridScheduleSerializers(show_grids, many=True)

        # cache.set(zip, serializer.data, timeout=600)

        return Response(serializer.data)

    def get_zip_code_from_coords(self, lat, long):

        url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=' + lat + ',' + long + '&sensor=true'

        res = requests.get(url)

        res = res.json()['results']

        zip_code = self.extract_zip_code_from_geocode(res)

        return zip_code

    def extract_zip_code_from_geocode(self, res):
        for i in res:
            for x in i['address_components']:
                if 'postal_code' in x['types']:
                    return x['long_name']

    def process_new_grid_listing(self, service_listings):
        satellite_service = [x for x in service_listings if x.data['SystemName'] == 'Dish Network'][0]
        sched = RoviAPI.get_grid_schedule_for_service_id(satellite_service)
        # sched = RoviAPI.process_chans_for_streaming(satellite_grid_list)

        grid_list = [sched]

        return grid_list

    def process_new_listings(self, service_listings, zip):
        s = RoviAPI.get_listings_for_zip_code(zip)
        s = json.loads(s)['ServicesResult']['Services']['Service']
        service_listings = [RoviAPI.save_listing(zip, x) for x in s if x['SystemName'] == 'Dish Network']
        return service_listings
