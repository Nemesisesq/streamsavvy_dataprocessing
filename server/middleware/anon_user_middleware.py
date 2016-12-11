from server.models import AnonymousUser
import time


class ProcessAnonUser(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            if not request.session.get('has_session'):
                request.session['has_session'] = True
                request.session.save()

            try:
                user = AnonymousUser.objects.get(session=request.session.session_key)
            except:
                user = AnonymousUser(session=request.session.session_key)
                user.is_authenticated()
                user.username = time.time()

            user.save()

            request.user = user
