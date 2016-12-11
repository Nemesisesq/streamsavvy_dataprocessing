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

from server.constants import sling_channels, broadcast_channels, banned_channels, allowed_services
from server.models import Content, Channel, Images, ChannelImages
from server.shortcuts import try_catch


def is_banned_channel(i, m):
    if type(i) == dict:
        return fuzz.token_sort_ratio(i['display_name'], m) >= 90
    else:
        return fuzz.token_sort_ratio(i.name, m) >= 90


@try_catch
def check_for_banned_service(i):
    matches = [m for m in banned_channels if is_banned_channel(i, m)]

    if matches:
        return False
    return True


@try_catch
def get_date_channels_last_checked(c):
    if c.channels_last_checked is not None:
        td = datetime.datetime.now(datetime.timezone.utc) - c.channels_last_checked
        return td.days > 30
    return True


class GuideBox(object):
    API_URL = 'api-public.guidebox.com'
    VERSION = 'v1.43'
    REGION = 'US'
    API_KEY = 'rKWvTOuKvqzFbORmekPyhkYMGinuxgxM'
    BASE_URL = "http://{API_URL}/{VERSION}/{REGION}/{API_KEY}".format(API_URL=API_URL, VERSION=VERSION, REGION=REGION,
                                                                      API_KEY=API_KEY)
    logger = logging.getLogger('cutthecord')

    # def __init__(self):

    def get_new_shows(self, time):
        new_show_url = "{BASE_URL}/updates/shows/new/{last_process_time}?limit=1&page={page}".format(BASE_URL=self.BASE_URL,
                                                                                                   last_process_time=time,
                                                                                                   page=1)
        try:
            with urllib.request.urlopen(new_show_url) as exact_response:
                the_json = json.loads(exact_response.read().decode('utf-8'))
            return the_json
        except:
            pass

    def get_total_number_of_shows(self, **kwargs):
        response = self.get_content_list(0, **kwargs)
        dict = json.loads(response)
        return dict['total_results']

    def get_total_number_of_channels(self):
        response = self.get_channel_list()
        dict = json.loads(response)
        return dict['total_results']

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

    @try_catch
    def process_content_for_sling_ota_banned_channels(self, c, search_query=False):

        c = self.check_for_sources_date_last_checked(c)

        c = self.remove_banned_channels(c)

        sources = c.guidebox_data['sources']['web']['episodes']['all_sources']

        sources = [self.check_for_sling(s) for s in sources]
        sources = [self.check_for_over_the_air(s) for s in sources]

        c.guidebox_data['sources']['web']['episodes']['all_sources'] = sources

        for s in c.channel.all():
            self.check_for_sling(s)

        c.guidebox_data['detail']['channels'] = [self.check_for_sling(s) for s in c.guidebox_data['detail']['channels']]
        c.guidebox_data['detail']['channels'] = [self.check_for_over_the_air(s) for s in c.guidebox_data['detail']['channels']]


        c.save()
        return c

    def check_for_over_the_air(self, s):
        if isinstance(s, Channel):
            if s.guidebox_data['name'] in broadcast_channels:
                s.guidebox_data['is_over_the_air'] = 'true'
                s.save()
                return s

        else:

            if 'display_name' in s and s['display_name'] in broadcast_channels:
                s['is_over_the_air'] = 'true'
                return s

            if 'name' in s and s['name'] in broadcast_channels:
                s['is_over_the_air'] = 'true'
                return s

        return s

    def check_for_sling(self, s):
        if isinstance(s, Channel):
            if s.guidebox_data['name'] in sling_channels:
                s.guidebox_data['on_sling'] = 'true'
                s.is_on_sling = True
                s.save()
                return s
        else:
            if 'display_name' in s and s['display_name'] in sling_channels:
                s['on_sling'] = 'true'

                return s
        return s

    def check_key_value(self, array, key, value):
        for i in array:

            if re.match(value, i[key]):
                return True

    @try_catch
    def remove_banned_channels(self, c):

        web_sources = c.guidebox_data['sources']['web']['episodes']['all_sources']
        ios_sources = c.guidebox_data['sources']['ios']['episodes']['all_sources']
        android_sources = c.guidebox_data['sources']['android']['episodes']['all_sources']

        source = {
            'w': web_sources,
            'i': ios_sources,
            'a': android_sources
        }

        for key in ['w', 'i', 'a']:

            x = self.filter_hulu_if_showtime(source[key], web_sources)

            if key == 'w':
                web_sources = x
            if key == 'i':
                ios_sources = x
            if key == 'a':
                android_sources = x

        c.guidebox_data['sources']['web']['episodes']['all_sources'] = []
        for i in web_sources:
            if type(i) is dict and i['display_name'] not in banned_channels:
                c.guidebox_data['sources']['web']['episodes']['all_sources'].append(i)

        c.guidebox_data['sources']['ios']['episodes']['all_sources'] = []
        for i in ios_sources:
            if type(i) is dict and i['display_name'] not in banned_channels:
                c.guidebox_data['sources']['ios']['episodes']['all_sources'].append(i)

        c.guidebox_data['sources']['android']['episodes']['all_sources'] = []
        for i in android_sources:
            if type(i) is dict and i['display_name'] not in banned_channels:
                c.guidebox_data['sources']['android']['episodes']['all_sources'].append(i)

        c.channel = [i for i in c.channel.all() if self.check_for_banned_service(i)]
        c.guidebox_data['sources']['web']['episodes']['all_sources'] = self.check_for_allowed_channels(
            c.guidebox_data['sources']['web']['episodes']['all_sources'])

        return c

    @try_catch
    def check_for_allowed_channels(self, list):

        res = []
        for i in list:
            x = [e for e in process.extract(i['display_name'], allowed_services) if e[1] > 80]

            if len(x) > 0:
                res.append(i)

        return res

    def filter_hulu_if_showtime(self, source, web_sources):
        x = []
        for i in web_sources:
            if re.match(r'hulu', i['source']):
                if self.check_key_value(source, 'source', 'showtime'):
                    pass
                else:
                    x.append(i)

            else:
                x.append(i)
        return x

    def check_for_sources_date_last_checked(self, c):
        # if cache.get(c.id):
        #     return c
        # c = self.add_additional_channels_for_show(c)
        # # c.channels_last_checked = datetime.datetime.now(datetime.timezone.utc)
        # c.save()
        #
        # cache.set(c.id, c.title)

        return c

    def add_additional_channels_for_show(self, shows):

        def execute(c):
            if type(c) is int:
                c = Content.objects.get(id=c)

            if c.guidebox_data:
                available_sources = json.loads(self.get_available_content_for_show(c.guidebox_data['id']))
                try:

                    c.guidebox_data['sources'] = available_sources['results']

                    # self.process_content_for_sling_ota_banned_channels(c)

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


        # def populate_content(self):
        # total_results = json.loads(self.get_content_list(0))['total_results']
        # show_count = 0
        # loop = True
        # count = 0
        # while loop:
        #     index = count * 250
        #     results = json.loads(self.get_content_list(index))
        #     if results['total_returned']:
        #         shows_dict = results['results']
        #         for i in shows_dict:
        #             show_count += 1
        #             self.save_content(i)
        #         count += 1
        #     else:
        #         loop = False
        #
        # return show_count

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

    def save_content(self, the_json):

        c = Content.objects.get_or_create(guidebox_data__id=the_json['id'])

        content = c[0]
        content.title = the_json['title']
        content.guidebox_data = the_json
        try:
            content.save()
            print("{0} was saved".format(c))
        except Exception as e:
            print(e)

        return content

    def save_content_detail(self, the_json):
        c = ''

        if type(the_json) is str:
            the_json = json.loads(the_json)

        c = Content.objects.get(guidebox_data__id=the_json['id'])

        c.guidebox_data['detail'] = the_json

        try:
            c.save()
            return True
        except Exception as e:
            return False

    def save_images(self, i):
        obj = Images()

        obj.thumbnail_small = i['artwork_208x117'] if i['artwork_208x117'] else None
        obj.thumbnail_medium = i['artwork_304x171'] if i['artwork_304x171'] else None
        obj.thumbnail_large = i['artwork_448x252'] if i['artwork_448x252'] else None
        obj.thumbnail_x_large = i['artwork_608x342'] if i['artwork_608x342'] else None

        if obj.save():
            return i

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

    def save_channel(self, the_json):

        c = Channel.objects.get_or_create(guidebox_data__id=the_json['id'])
        chan = c[0]

        chan.name = the_json['name'] if the_json['name'] else None
        chan.guidebox_data = the_json

        matches = [c for c in sling_channels if fuzz.token_set_ratio(chan.name, c) >= 90]
        if matches:
            chan.is_on_sling = True

        chan.save()

        return chan

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
                                        content = self.save_content(show)
                                    else:
                                        content = c_tuple[0]

                                    content.channel.add(chan)

                                    content.save()
                                except Exception as e:
                                    print(e)
            except Exception as e:
                self.logger.error(e)

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

    def process_channels_for_images(self, channel):
        try:

            res = self.get_channel_images(channel)

            images = res['results']

            imgs = ChannelImages(guidebox_id=channel, data=images)

            imgs.save()

            return imgs



        except Exception as e:
            print(e)

    @try_catch
    def check_for_banned_service(self, i):
        matches = [m for m in banned_channels if is_banned_channel(i, m)]

        if matches:
            return False
        return True
