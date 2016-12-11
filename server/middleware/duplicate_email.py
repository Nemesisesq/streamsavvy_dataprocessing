from rest_framework_jwt.settings import api_settings

class DuplicateEmail(object):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if response.status_code is 500:
            pass
