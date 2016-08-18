import json

import itertools
from multiprocessing.dummy import Pool

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import token_sort_ratio, token_set_ratio

from data_processor.models import Sport, Schedule
from data_processor.shortcuts import try_catch

ncaaf_teams = Sport.objects.filter(category='College Football')

sport_data = [i.title.replace('Football', '') for i in ncaaf_teams]
tag_data = [i.json_data['nickname'] for i in ncaaf_teams]


@try_catch
def add_ncaaf_schedules():
    with open('ncaaf_08_17_2016.json') as json_data:
        data = json.load(json_data)

    # pool = Pool(30)
    # results = pool.map(process_data, data)
    # pool.close()
    # pool.join()

    for i in data:
        process_data(i, )

        # print(results)


def process_data(raw_data):
    sched = Schedule()
    sched.team_name = raw_data['name'] if type(raw_data['name']) is str else raw_data['name'][0]
    sched.data = raw_data['games']
    sched.team_logo = raw_data['logo']
    sched_team_name = raw_data['name'][0]

    if sched_team_name == 'Northern Illinois Huskies':
        sched_team_name = sched_team_name.replace('Northern Illinois', 'NIU')

    if sched_team_name == 'Southern Mississippi Golden Eagles':
        sched.team = Sport.objects.get(title='Southern Miss Football')
        sched.save()
        return

    if sched_team_name == 'TCU Horned Frogs':
        sched.team = Sport.objects.get(title='TCU Football')
        sched.save()
        return

    by_name = process.extract(sched_team_name, sport_data, scorer=token_sort_ratio)
    by_nick = process.extract(sched_team_name, tag_data, limit=10)
    name_obj = [Sport.objects.filter(title__startswith=x[0]) for x in by_name]
    nick_obj = [Sport.objects.filter(json_data__nickname=x[0]) for x in by_nick]
    name_obj_list = list(itertools.chain.from_iterable(name_obj))
    nick_obj_list = list(itertools.chain.from_iterable(nick_obj))
    result = [i for i in nick_obj_list if i in [d for d in name_obj_list]]

    if result:
        sched.team = result[0]
    else:
        sched.team = nick_obj_list[0]

    sched.team.json_data['logo'] = raw_data['logo']
    sched.team.save()

    sched.save()
