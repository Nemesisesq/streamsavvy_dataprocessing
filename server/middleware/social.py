from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from django.core.cache import cache
from urllib.parse import urlparse

from server.models import Package


class SaveInitialPackage():
    def process_request(self, request):
        if 'pkg' in request.GET:
            anon_pkg = request.GET['pkg']
            parsed_url = urlparse(anon_pkg)
            pkg_id = [i for i in parsed_url.path.split('/') if i][-1]
            anon_user = request.GET['anon_user']
            cache.set(anon_user, pkg_id)



    def process_response(self, request, response):
        # try:
        #     anon_user = request.GET['anon_user']
        #     if anon_user != request.user.username:
        #         id = cache.get(anon_user)
        #         pkg = Package.objects.get(pk=id)
        #
        #         if request.user.is_authenticated():
        #             request.user.packages.data = pkg.data
        #             request.user.save()
        #             request.user.packages.save()
        #             old_user = User.objects.get(username=anon_user)
        #             old_user.delete()
        #
        # except Exception as e:
        #     print(e)



        return response
