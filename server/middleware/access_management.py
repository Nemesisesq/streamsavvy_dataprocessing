import json
import logging
import os
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from server.shortcuts import api_json_post

__author__ = 'Nem'


class BlockLiveSiteFromNonAdminUsers(object):

    logger = logging.getLogger('cutthecord')

    def process_request(self, request):

        # os.environ['ENVIRONMENT']= 'production'
        re = request
        self.logger.debug('Checking environment {} for user {}'.format(os.getenv('Environment'), re.user))
        if os.getenv('ENVIRONMENT') == 'production' and os.getenv('REQUIRE_AUTH'):
            if request.user.is_staff or request.user.is_authenticated or request.path_info.startswith('/admin/'):
                return None

            elif request.path_info.startswith('/beta/'):
                return None

            else:
                return redirect('http://www.streamsavvy.tv')

        else:
            return None

class DisableCSRF(object):
    def process_request(self, request):
            setattr(request, '_dont_enforce_csrf_checks', True)


class LogUserIfExistsForSignUp(object):


    def process_request(self, request):
        if( request.path == '/sign_up/'):


            the_json = json.loads(str(request.body, encoding='utf-8'))

            try:
                user =  authenticate(username=the_json['username'], password=the_json['password'])

                request.user = user
            except:
                pass


        pass
