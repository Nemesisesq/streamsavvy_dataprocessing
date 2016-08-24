import datetime
import json
import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from data_processor.constants import banned_channels, broadcast_channels, allowed_services, sling_channels
from data_processor.models import Channel, Content
from data_processor.shortcuts import try_catch


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


def check_for_over_the_air(s):
    if isinstance(s, Channel):
        if s.guidebox_data['name'] in broadcast_channels:
            s.guidebox_data['is_over_the_air'] = 'true'
            s.save()
            return s

    else:

        if 'display_name' in s and s['display_name'] in broadcast_channels:
            s['is_over_the_air'] = 'true'
            return s

    return s


@try_catch
def check_for_allowed_channels(list):
    res = []
    for i in list:
        x = [e for e in process.extract(i['display_name'], allowed_services) if e[1] > 80]

        if len(x) > 0:
            res.append(i)

    return res


@try_catch
def check_for_banned_service(i):
    matches = [m for m in banned_channels if is_banned_channel(i, m)]

    if matches:
        return False
    return True


def save_channel(the_json):
    c = Channel.objects.get_or_create(guidebox_data__id=the_json['id'])
    chan = c[0]

    chan.name = the_json['name'] if the_json['name'] else None
    chan.guidebox_data = the_json

    matches = [c for c in sling_channels if fuzz.token_set_ratio(chan.name, c) >= 90]
    if matches:
        chan.is_on_sling = True

    chan.save()

    return chan


def save_content(the_json):
    try:
        c = Content.objects.get(guidebox_data__id=the_json['id'])
        content = c[0]

    except:
        content = Content()

    content.title = the_json['title']
    content.guidebox_data = the_json
    try:
        content.save()
        print("{0} was saved".format(c))
    except Exception as e:
        print(e)

    return content


def save_content_detail(the_json):
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


def check_key_value(array, key, value):
    for i in array:

        if re.match(value, i[key]):
            return True


def filter_hulu_if_showtime(source, web_sources):
    x = []
    for i in web_sources:
        if type(i) is dict and re.match(r'hulu', i['source']):
            if check_key_value(source, 'source', 'showtime'):
                pass
            else:
                x.append(i)

        else:
            x.append(i)
    return x


def check_for_sling(s):
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

@try_catch
def remove_banned_channels(c):

    web_sources = c.guidebox_data['sources']['web']['episodes']['all_sources']
    ios_sources = c.guidebox_data['sources']['ios']['episodes']['all_sources']
    android_sources = c.guidebox_data['sources']['android']['episodes']['all_sources']

    source = {
        'w': web_sources,
        'i': ios_sources,
        'a': android_sources
    }

    for key in ['w', 'i', 'a']:

        x = filter_hulu_if_showtime(source[key], web_sources)

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

    c.channel = [i for i in c.channel.all() if check_for_banned_service(i)]
    c.guidebox_data['sources']['web']['episodes']['all_sources'] = check_for_allowed_channels(
        c.guidebox_data['sources']['web']['episodes']['all_sources'])

    return c

@try_catch
def process_content_for_sling_ota_banned_channels(c, search_query=False):

    # self.check_for_sources_date_last_checked(c)

    c = remove_banned_channels(c)

    sources = c.guidebox_data['sources']['web']['episodes']['all_sources']

    sources = [check_for_sling(s) for s in sources]
    sources = [check_for_over_the_air(s) for s in sources]

    c.guidebox_data['sources']['web']['episodes']['all_sources'] = sources

    for s in c.channel.all():
        check_for_sling(s)

    c.save()
    return c
