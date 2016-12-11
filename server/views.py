import json
import logging
import time
import urllib
import urllib.parse
import urllib.request
from multiprocessing.pool import Pool

import requests
from django.core.cache import cache
from django.db.models import Max, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fuzzywuzzy import fuzz
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from social.actions import do_complete
from social.apps.django_app.utils import strategy
from social.apps.django_app.views import _do_login

from server.apis.guidebox import GuideBox
from server.auth import create_jwt
from server.constants import unwanted_show_ids
from server.models import *
from server.permissions import IsAdminOrReadOnly
from server.permissions import IsAuthenticatedOrCreate
from server.serializers import HardwareSerializer, ChannelSerializer, \
    ContentSerializer, PackagesSerializer, SignUpSerializer, UserSerializer
from server.shortcuts import api_json_post, try_catch
from streamsavvy_webapp.settings import get_env_variable

logger = logging.getLogger(__name__)


def get_sign_up_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token


def flatten(l):
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def get_user(self):
    if self.request.user.is_anonymous():
        if not self.request.session.get('has_session'):
            self.request.session['has_session'] = True
            self.request.session.save()
        try:
            user = AnonymousUser.objects.get(session=self.request.session.session_key)
        except:
            user = AnonymousUser(session=self.request.session.session_key)
            user.username = time.time()

        user.save()


    else:
        user = self.request.user

    return user


def get_packages(user):
    package = Package.objects.filter(owner=user)

    if not package:
        Package(owner=user).save()
        package = Package.objects.filter(owner=user)

    return package


def check_token_is_valid():
    pass


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def post(self, request, *args, **kwargs):
        try:

            if 'username' in request.POST:
                credentials = {
                    'username': request.POST['username'],
                    'email': request.POST['email'],
                    'password': request.POST['password']
                }
            elif 'username' in request._data:
                credentials = {
                    'username': request._data['username'],
                    'email': request._data['email'],
                    'password': request._data['password']
                }

            else:

                credentials = json.loads(str(request.body, encoding='utf-8'))

            token = create_jwt(credentials)

            if not token:
                response = self.create(request, *args, **kwargs)
                token = create_jwt(credentials)
                return Response({"token": str(token)}, status=status.HTTP_201_CREATED)

            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"error": "User already Exists or Password Invalid "}, status=status.HTTP_401_UNAUTHORIZED)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # print(response.data['username'])
        # user = User.objects.get(username=response.data['username'])

        # TODO this is a hack and neeeds to be properly fixed
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
        # login(request, user)
        # response['token'] = get_sign_up_token(user)
        return response


class AdminPermMixin(object):
    permission_classes = (IsAdminOrReadOnly,)


class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    http_method_names = ['get']


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    http_method_names = ['get']

    def get_object(self):
        obj = super(ContentViewSet, self).get_object()
        g = GuideBox()

        if 'detail' in obj.guidebox_data:
            obj = g.process_content_for_sling_ota_banned_channels(obj, True)
            obj.save()
            return obj

        else:
            detail = g.get_content_detail(obj.guidebox_data['id'])
            detail = json.loads(detail)

            obj.guidebox_data['detail'] = detail

            obj = g.process_content_for_sling_ota_banned_channels(obj, True)

            obj.save()
            return obj


class PopularShowsViewSet(viewsets.ModelViewSet):
    # queryset = get_popular_shows()
    serializer_class = ContentSerializer
    http_method_names = ['get']

    def get_queryset(self):
        res = Content.objects.annotate(p=Max('popularity__score')).annotate(p_count=Count('popularity')).exclude(
            p_count=0).order_by('-p')

        filter_results = [x for x in res if x.guidebox_data and x.guidebox_data['id'] not in unwanted_show_ids]

        # banned server

        filter_results = [show for show in filter_results if show.id != 15296]

        return filter_results


class PackagesViewSet(viewsets.ModelViewSet):
    serializer_class = PackagesSerializer
    http_method_names = ['get', 'put']

    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = get_user(self)

        try:
            pkg = user.packages
        except Exception as e:
            pkg = False

        if 'anon_user' in self.request.GET and not pkg:
            anon_user = self.request.GET['anon_user']
            try:

                if self.request.user.is_authenticated():
                    id = cache.get(anon_user)
                    pkg = Package.objects.get(pk=id)

                    package = get_packages(user)
                    x = package[0]
                    x.data = pkg.data
                    x.save()
                    # pkg.delete()
                    # anon_user.delete()

                    package = [x]

                else:
                    package = get_packages(user)


            except Exception as e:
                package = get_packages(user)
        else:
            package = get_packages(user)

        return package


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_name = ['get', 'put']

    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = get_user(self)

        return [user]


def eval_string(d):
    d['guidebox_data'] = eval(d['guidebox_data'])

    return d


def simple_relevance_score(q, show):
    nick_score = 0

    if 'category' in show:
        show['curr_pop_score'] = 1.5

        if 'nickname' in show['json_data']:
            nick_score = fuzz.token_sort_ratio(q, show['json_data']['nickname'])

    raw_score = fuzz.token_sort_ratio(q, show['title']) + nick_score

    weighted_score = raw_score * show['curr_pop_score']
    return weighted_score


@try_catch
def call_search_microservice(request):
    if request.GET['q']:

        query_url = "{base}/search/?{params}".format(base=get_env_variable('DATA_MICROSERVICE_URL'),
                                                     params=urllib.parse.urlencode({'q': request.GET['q']}))

        sports_query = "{base}/search_sports/?{params}".format(base=get_env_variable('DATA_MICROSERVICE_URL'),
                                                               params=urllib.parse.urlencode({'q': request.GET['q']}))
        urls = [query_url]
        # urls = [sports_query, query_url]  # TODO Uncomment when there is more data to support sports

        pool = Pool(processes=len(urls))
        results = pool.map(requests.get, urls)
        pool.close()
        pool.join()

        result_list = []

        for response in results:
            try:
                result_list += response.json()

            except Exception as e:
                print(e)

        result_list = sorted(result_list, key=lambda show: simple_relevance_score(request.GET['q'], show), reverse=True)

        return JsonResponse(result_list, safe=False)


@try_catch
@api_json_post
def get_service_list(request, the_json, path):
    query_url = ""

    if path == 'servicelist':
        query_url = method_name('service_list')

    if path == 'checkoutlist':
        query_url = method_name('checkout_list')

    if path == 'detailsources':
        query_url = method_name('detail_sources')

    if path == 'sonyVue':
        query_url = method_name('sling_vue')

    try:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(query_url, data=json.dumps(the_json), headers=headers)
        d = r.json()

        d = json.dumps(d)
        d = json.loads(d)
        return JsonResponse(d, safe=False)
    except Exception as e:
        print(e)


def method_name(path):
    return "{base}/{path}".format(base=get_env_variable('NODE_DATA_SERVICE'), path=path)


@try_catch
def get_service_description(request, service):
    if request.method == 'GET':
        query_url = "{base}{path}".format(base=get_env_variable('DATA_MICROSERVICE_URL'), path=request.path)
        try:
            r = requests.get(query_url)
            return JsonResponse(r.json(), safe=False)
        except Exception as e:
            print(e)


def get_viewing_windows(request, service):
    if request.method == 'GET':
        query_url = "{base}/window/?q={service}".format(base=get_env_variable('DATA_MICROSERVICE_URL'), service=service)
        try:
            r = requests.get(query_url)
            return JsonResponse(r.json(), safe=False)
        except Exception as e:
            print(e)


@csrf_exempt
@strategy('social:complete')
def complete(request, backend, *args, **kwargs):
    """Override this method so we can force user to be logged out."""
    return do_complete(request.social_strategy, _do_login, user=None,
                       redirect_name='/', *args, **kwargs)


def get_module_description(request, category=None):
    if request.method == 'GET':
        query_url = "{base}/modules/?q={category}".format(base=get_env_variable('DATA_MICROSERVICE_URL'),
                                                          category=category)
        try:
            r = requests.get(query_url)
            return JsonResponse(r.json(), safe=False)
        except Exception as e:
            print(e)


@api_json_post
def post_edr_data(request, the_json):
    if request.method == 'POST':
        query_url = "{edr_data_service}".format(edr_data_service=get_env_variable('EDR_DATA_SERVICE'))
        try:
            headers = {'Content-Type': 'application/json'}
            r = requests.post(query_url, data=json.dumps(the_json), headers=headers)
            d = r.json()

            d = json.dumps(d)
            d = json.loads(d)
            return JsonResponse(d, safe=False)
        except Exception as e:
            print(e)


def get_sport_schedule(request, sport_id):
    if request.method == 'GET':
        query_url = "{base}/sport_schedule/{sport_id}".format(base=get_env_variable('DATA_MICROSERVICE_URL'),
                                                              sport_id=sport_id)
        try:
            r = requests.get(query_url)

            url = method_name('sched_suggestion')

            headers = {'Content-Type': 'application/json'}
            sug_r = requests.post(url, data=json.dumps(r.json()), headers=headers)
            print(sug_r, 'prob')

            return JsonResponse(sug_r.json(), safe=False)
        except Exception as e:
            print(e)
            Response(e)
