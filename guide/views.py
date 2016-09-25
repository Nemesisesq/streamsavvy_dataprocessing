import datetime
import json
import logging
import urllib
from multiprocessing.dummy import Pool

import re
from time import sleep

import pytz
import requests
from celery import shared_task
from celery.task import task
from django.core.cache import cache
from fuzzywuzzy import fuzz
from pymongo import MongoClient
from rest_framework.response import Response
from rest_framework.views import APIView

from data_processor.tasks import scraper_example
from guide.models import RoviListings, RoviGridSchedule, RoviProgramImages
from guide.serializers import RoviGridScheduleSerializers
from data_processor.constants import sling_channels, live_channel_filter_list
from data_processor.shortcuts import lazy_thunkify, try_catch, api_json_post
from streamsavvy_dataprocessing.celery import app
from streamsavvy_dataprocessing.settings import get_env_variable

logger = logging.getLogger('cutthecord')


class RoviAPI(object):
    # api_key = 'rj5pcy96h2uee7gmesf755ay'
    api_key = 'p3nh3333exq3umj9ka8uqhee'  # Key for the siceone account on rovi
    BASE_URL = 'http://api.rovicorp.com/TVlistings/v9/listings/'

    @classmethod
    @try_catch
    def get_images_for_show_id(cls, program_id):
        print('im making call to rovi')
        program_detail_url = "{}programdetails/{}/info?".format(cls.BASE_URL, program_id)
        params = {'local': 'en-US',
                  'copytextformat': 'PlainText',
                  'include': 'Image',
                  'imagecount': 5,
                  'duration': 20160,
                  'format': 'json',
                  'apikey': '9d4zzdxbzvguqgykwjnz2g7n',

                  }

        url = program_detail_url + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = json.loads(response.read().decode('utf-8'))
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return {}

    @classmethod
    def get_listings_for_zip_code(cls, zip):

        listing_url = "{}services/postalcode/{}/info?".format(cls.BASE_URL, zip)
        params = {
            'locale': 'en-US',
            'countrycode': 'US',
            'format': 'json',
            'apikey': cls.api_key,
            'sourceFilterExclude': 'HD, PPV, Music'
        }

        url = listing_url + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return {}

    @classmethod
    @try_catch
    def retrieve_schedule_from_db(cls, zipcode):
        return RoviGridSchedule.objects.filter(postal_code=zipcode).latest('date_added')

    @classmethod
    def get_schedule_from_rovi_api(cls, service_id):

        listing_url = "{}gridschedule/{}/info?".format(cls.BASE_URL, service_id)
        params = {
            'locale': 'en-US',
            'duration': 60,
            'includechannelimages': 'true',
            'format': 'json',
            'apikey': cls.api_key
        }

        url = listing_url + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return {}

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

        grid_obj = cls.save_channel_grid(service_id.postal_code, sched)

        grid_obj = cls.fix_show_time(grid_obj)

        grid_obj.save()
        # sched = cls.process_chans_for_streaming(sched)


        return sched

    @classmethod
    def fix_show_time(cls, sched):

        offset = sched.data['GridScheduleResult']['TimeZones'][0]['Offset']
        for i in sched.data['GridScheduleResult']['GridChannels']:
            for a in i['Airings']:
                utc_time = a['AiringTime'].replace('Z', 'UTC')

                z = datetime.datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S%Z')
                # z = pytz.utc.localize(z)
                td = datetime.timedelta(minutes=offset)
                fixed_time = z + td

                a['AiringTime'] = fixed_time.strftime('%Y-%m-%dT%H:%M:%S%Z') + 'Z'

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

        filter_list = live_channel_filter_list

        filter_chans = sched['GridScheduleResult']['GridChannels']

        filter_chans = [x for x in filter_chans if not re.search(r"HD", x['CallLetters'])]

        filter_chans = [x for x in filter_chans if not re.search(r"SPRTS", x['CallLetters'])]

        filter_chans = [x for x in filter_chans if not re.search(r"TVB", x['CallLetters'])]

        filter_chans = [x for x in filter_chans if not re.search(r"ET", x['CallLetters'])]

        filter_chans = [x for x in filter_chans if x['Order'] < 6000000]

        filter_chans = [x for x in filter_chans if not x['SourceAttributes'] == '8']

        filter_chans = [x for x in filter_chans if not re.search(r"HD", x['SourceLongName'])]

        filter_chans = [x for x in filter_chans if not re.search(r"Mid-Atlantic", x['SourceLongName'])]

        filter_chans = [x for x in filter_chans if not re.search(r"DISH", x['CallLetters'])]

        filter_chans = [x for x in filter_chans if not re.search(r"CSN", x['CallLetters'])]

        filter_chans = [x for x in filter_chans if not re.search(r"ALT", x['CallLetters'])]

        filtered_chans = []
        for x in filter_chans:
            letters_ = x['CallLetters']
            if letters_ not in filter_list:
                filtered_chans.append(x)

        filtered_chans = cls.remove_duplicates(filtered_chans)

        sched['GridScheduleResult']['GridChannels'] = filtered_chans

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

        hello.delay()

        scraper_example.delay(3,4)

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

        # show_grids = [RoviAPI.fix_show_time(g) for g in show_grids]

        get_program_images.delay(show_grids)

        serializer = RoviGridScheduleSerializers(show_grids, many=True)

        # cache.set(zip, serializer.data, timeout=600)

        return Response(serializer.data)

    def get_zip_code_from_coords(self, lat, long):

        url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key=AIzaSyBKbr-04-_phVgOMbr1xwQD9CBi-fHZ0QY'
        url = url.format(lat=lat, long=long)
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
        res = RoviAPI.get_listings_for_zip_code(zip)
        the_json = json.loads(res)
        services = the_json['ServicesResult']['Services']['Service']
        service_listings = [RoviAPI.save_listing(zip, x) for x in services if x['SystemName'] == 'Dish Network']
        return service_listings



@shared_task(name='cell test')
def hello():
    print('world')

@shared_task(name='get_async_show_images')
def get_program_images(show_grids):

    for chan in show_grids[0].data['GridScheduleResult']['GridChannels']:
        for airing in chan['Airings']:
            if 'images' not in airing:
                images = get_show_images(airing['ProgramId'])
                airing['images'] = images['ProgramDetailsResult']['Program']['ProgramImages']

                show_grids[0].save()


@try_catch
def get_show_images(show_id):
    print('imf iring')
    client = MongoClient(get_env_variable('MONGODB_URI'))
    db = client.roviDb
    collection = db.showImages

    img = collection.find_one({"showId": show_id})
    if not img:
        sleep(.2)
        logger.info("{} not found".format(show_id))
        res = get_images_for_show_id(show_id)
        res["showId"] = show_id
        collection.insert_one(res)
        return res
    else:
        logger.info("{} found".format(show_id))

    return img

@try_catch
def get_images_for_show_id(program_id):
    print('im making call to rovi')
    program_detail_url = "{}programdetails/{}/info?".format(RoviAPI.BASE_URL, program_id)
    params = {'local': 'en-US',
              'copytextformat': 'PlainText',
              'include': 'Image',
              'imagecount': 5,
              'duration': 20160,
              'format': 'json',
              'apikey': '9d4zzdxbzvguqgykwjnz2g7n',

              }
    url = program_detail_url + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url) as response:
            the_json = json.loads(response.read().decode('utf-8'))
        return the_json
    except urllib.error.URLError as e:
        print(e)
        return {}
