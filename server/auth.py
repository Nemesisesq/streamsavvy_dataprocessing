import time
import jwt
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import authentication, exceptions

from django.conf import settings
from social.apps.django_app.default.models import UserSocialAuth

__author__ = 'Nem'
from django.contrib.auth import authenticate, login
from server.shortcuts import api_json_post
from social.apps.django_app.utils import psa


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        login(request, user)

        social = user.social_auth

        jwt_token = create_token('', user, social=social)

        return jwt_token
    else:
        return 'ERROR'




current_milli_time = lambda: int(round(time.time() * 1000))


@api_json_post
def login_view(request, the_json):
    username = the_json['username']
    password = the_json['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)

            return JsonResponse({'success': 'Welcome {user}'.format(user=user.first_name),
                                 'messages': [
                                     {"text": "Logged In Successfully Welcome {user}".format(user=user.first_name),
                                      "severity": "success"}
                                 ]})
        else:
            return JsonResponse({'error': 'there seems to be a problem with your username or password'})
    else:
        return JsonResponse({'error': 'this user does not exsist'})


def create_jwt(the_json, *args, **kwargs):
    username = the_json['username']
    password = the_json['password']

    user = authenticate(username=username, password=password)

    if not user:
        return False
    return create_token(password, user)


def create_token(password, user, *args, **kwargs):
    user_dict = model_to_dict(user,
                              fields=['created', 'email', 'username', 'password'])
    user_dict['password'] = password

    if kwargs:
        user_dict['social'] = kwargs['social']
    payload = user_dict
    time = current_milli_time()
    payload['token_created'] = time
    secret_key = getattr(settings, "SECRET_KEY")
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token


def get_user(token):
    payload = decode_token(token)

    try:
        u = User.objects.get(username=payload['username'], password=payload['password'])
    except Exception as e:
        raise e

    return u


def check_token(token):
    payload = decode_token(token)

    try:
        if 'social' in payload:
            u = UserSocialAuth.objects.get(uid=payload['social']['uid'])
        else:
            u = authenticate(username=payload['username'], password=payload['password'])
    except Exception as e:

        return False

    if (current_milli_time() - payload['token_created']) > 7776000000:
        return False

    return u


def decode_token(token):
    secret_key = getattr(settings, "SECRET_KEY")
    payload = jwt.decode(token, secret_key, algorithm='HS256')
    return payload


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.META.get('HTTP_AUTHORIZATION').replace('Bearer_', '')

        if not token:
            return None

        # TODO some duplication in here but it's acceptable.


        try:
            u = check_token(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed('No such user')

        user = u

        return user
