from server.models import Profile

class DeviceIDMiddleWare(object):
    def process_request(self, request):
        try:
            request
        except Exception as e:
            pass
        finally:
            pass



