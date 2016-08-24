import datetime
import json
import logging
# import threading
import re
import urllib
import urllib.error
import urllib.request
# from queue import Queue
from django.core.cache import cache
from fuzzywuzzy import fuzz, process

from data_processor.constants import sling_channels, broadcast_channels, banned_channels, allowed_services
from data_processor.data_helper import is_banned_channel, save_content, check_for_allowed_channels, \
    check_for_banned_service, filter_hulu_if_showtime, check_for_sling, check_for_over_the_air
from data_processor.models import Content, Channel
from data_processor.shortcuts import try_catch, asynchronous


class GuideBox(object):
    API_URL = 'api-public.guidebox.com'
    VERSION = 'v1.43'
    REGION = 'US'
    API_KEY = 'rKWvTOuKvqzFbORmekPyhkYMGinuxgxM'
    BASE_URL = "http://{API_URL}/{VERSION}/{REGION}/{API_KEY}".format(API_URL=API_URL, VERSION=VERSION, REGION=REGION,
                                                                      API_KEY=API_KEY)
    logger = logging.getLogger('cutthecord')

    # def __init__(self):



    """
    This method returns the total number of shows in the from the guidebox api
    This was created to get a show count to populate the database with shows
    """

    def get_total_number_of_shows(self, **kwargs):
        response = self.get_content_list(0, **kwargs)
        dict = json.loads(response)
        return dict['total_results']

    """
    This method was created to get the total number of channels
    """

    def get_total_number_of_channels(self):
        response = self.get_channel_list()
        dict = json.loads(response)
        return dict['total_results']

    """
    This method was created to search for shows that weren't in the database upon searching.
    """

    def get_show_by_title(self, title):
        cleaned_title = title.replace("  ", " ")
        title, sep, cruft = cleaned_title.partition("-")
        encoded_show = title.strip().replace(" ", '%25252B')
        fuzzy_url = "{BASE_URL}/search/title/{TRIPLE_URL}/fuzzy".format(BASE_URL=self.BASE_URL, TRIPLE_URL=encoded_show)
        try:
            with urllib.request.urlopen(fuzzy_url) as exact_response:
                the_json = json.loads(exact_response.read().decode('utf-8'))
            return the_json
        except:
            pass

    def get_channel_images(self, id):

        fuzzy_url = "{BASE_URL}/channel/{ID}/images/all".format(BASE_URL=self.BASE_URL, ID=id)
        try:
            with urllib.request.urlopen(fuzzy_url) as exact_response:
                the_json = json.loads(exact_response.read().decode('utf-8'))
            return the_json
        except Exception as e:
            pass

    """
    This method was created to find the sources of shows.
    """

    def get_sources(self):
        url = "{BASE_URL}/sources/all/all".format(BASE_URL=self.BASE_URL)
        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
        return False

    def get_channels(self, content_id):
        url = "{BASE_URL}/show/{id}/available_content".format(BASE_URL=self.BASE_URL, id=content_id)
        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False

    def get_content_detail(self, content_id):
        url = "{BASE_URL}/show/{id}".format(BASE_URL=self.BASE_URL, id=content_id)
        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False

    def get_content_list(self, index, **kwargs):
        channel = kwargs['channel'] if 'channel' in kwargs else 'all'
        source = kwargs['source'] if 'source' in kwargs else 'all'
        platform = kwargs['platform'] if 'platform' in kwargs else  'all'
        url = "{BASE_URL}/shows/{channel}/{index}/250/{source}/{platform}".format(BASE_URL=self.BASE_URL,
                                                                                  index=index,
                                                                                  channel=channel,
                                                                                  source=source,
                                                                                  platform=platform)
        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False





    def get_sources_for_show(self, shows):

        def execute(c):
            if c.guidebox_data:
                available_sources = json.loads(self.get_available_content_for_show(c.guidebox_data['id']))
                try:

                    c.guidebox_data['sources'] = available_sources['results']

                    c.save()

                # TODO set up logging for this exception
                except Exception as e:
                    print(e)

        if type(shows) is list:
            for c in shows:
                execute(c)
        else:
            execute(shows)

        return shows

    @try_catch
    def get_available_content_for_show(self, content_id):
        url = "{BASE_URL}/show/{id}/available_content".format(BASE_URL=self.BASE_URL, id=content_id)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False

    def get_channel_list(self, type='all', start=0, limit=50):
        url = "{BASE_URL}/channels/{type}/{start}/{limit}".format(BASE_URL=self.BASE_URL, type=type, start=start,
                                                                  limit=limit)

        try:
            with urllib.request.urlopen(url) as response:
                the_json = response.read().decode('utf-8')
            return the_json
        except urllib.error.URLError as e:
            print(e)
            return False

    def connect_channels_shows(self, channel_list):
        print(channel_list)
        for chan in channel_list:
            try:
                if chan.guidebox_data:
                    length = self.get_total_number_of_shows(channel=chan.guidebox_data['short_name'])
                    if length:
                        for i in range(0, length, 24):
                            res = self.get_content_list(i, channel=chan.guidebox_data['short_name'])
                            shows = json.loads(res)['results']
                            for show in shows:

                                try:
                                    c_tuple = Content.objects.get_or_create(guidebox_data__id=show['id'])
                                    if c_tuple[1]:
                                        content = save_content(show)
                                    else:
                                        content = c_tuple[0]

                                    content.channel.add(chan)

                                    content.save()
                                except Exception as e:
                                    print(e)
            except Exception as e:
                self.logger.error(e)

    """
    This method processes shows fand add the content details for the show

    """

    def process_shows_for_content_detail(self, show_list):
        for show in show_list:
            try:
                if show.guidebox_data:
                    res = self.get_content_detail(show.guidebox_data['id'])

                    details = json.loads(res)
                    show.guidebox_data['detail'] = details

                    show.save()


            except Exception as e:
                print(e)
