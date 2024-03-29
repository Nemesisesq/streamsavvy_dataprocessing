from django.db.models import Q, Max, Count
from django.http import JsonResponse
from fuzzywuzzy import process
from haystack.query import SearchQuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from data_processor.constants import unwanted_show_ids
from data_processor.data_helper import process_content_for_sling_ota_banned_channels, save_content
from data_processor.guidebox import GuideBox
from data_processor.models import ServiceDescription, Channel, Content, ViewingServices, ModuleDescriptions, Schedule, \
    Sport
from data_processor.serializers import ServiceDescriptionSerializer, ContentSerializer, ChannelSerializer, \
    ViewingServicesSerializer, ModuleDescriptionSerializer, SportSerializer, ScheduleSerializer
from streamsavvy_dataprocessing.settings import get_env_variable


class ServiceDescriptionViewSet(viewsets.ModelViewSet):
    queryset = ServiceDescription.objects.all()
    serializer_class = ServiceDescriptionSerializer
    lookup_field = 'slug'


class ModuleDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleDescriptionSerializer

    def get_queryset(self):

        if 'q' in self.request.query_params:
            category = self.request.query_params['q'].strip().lower()

            return ModuleDescriptions.objects.filter(category__iexact=category)
        else:
            return ModuleDescriptions.objects.all()


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ViewingServicesViewSet(viewsets.ModelViewSet):
    queryset = ViewingServices.objects.all()
    serializer_class = ViewingServicesSerializer

    def get_queryset(self):
        q = self.request.GET['q'].strip()

        w = [i.name for i in ViewingServices.objects.all()]

        res = process.extract(q, w, limit=1)

        t = [ViewingServices.objects.get(name=res[0][0])]

        return t


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_object(self):
        obj = super(ContentViewSet, self).get_object()

        obj = process_content_for_sling_ota_banned_channels(obj)

        return obj


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class SearchSportsViewSet(viewsets.ModelViewSet):
    q = ""

    serializer_class = SportSerializer

    def get_queryset(self):

        self.q = self.request.GET.get('q', '')

        if get_env_variable('ENVIRONMENT') != 'PRODUCTION':

            sqs = SearchQuerySet().autocomplete(team_auto=self.q)[:20]

            suggestions = [result.object for result in sqs]

        else:
            suggestions = []

        return suggestions


class SearchContentViewSet(viewsets.ModelViewSet):
    q = ""
    serializer_class = ContentSerializer

    def get_queryset(self):

        self.q = self.request.GET.get('q', '')

        sqs = SearchQuerySet().autocomplete(content_auto=self.q)[:10]

        sqs_meta = SearchQuerySet().autocomplete(meta_auto=self.q)[:10]

        suggestions = [result.object for result in sqs] + [result.object for result in sqs_meta]

        filter_results = suggestions

        filter_results = [x for x in filter_results if x.guidebox_data['id'] not in unwanted_show_ids]

        filter_results = [show for show in filter_results if show.id != 15296]

        filter_results = list(reversed(sorted(filter_results, key=self.get_score)))

        return filter_results

    def get_score(self, obj):
        return obj.curr_pop_score

    def check_guidebox_for_query(self, filter_results, query_string):
        if len(filter_results) == 0:
            g = GuideBox()

            if ('q' in self.request.GET) and self.request.GET['q'].strip():
                result = g.get_show_by_title(query_string)

                result = result['results']

                result_list = []

                for show in result:
                    result_list.append(save_content(show))

                filter_results = self.filter_query([165], result_list)

        return filter_results

    def filter_content_by_guidebox_id(self, x):

        if x.guidebox_data['id'] not in [3084, 31168, 31150, 15935]:
            return True

        return False

    def filter_query(self, filtered_ids, entries):

        for i in filtered_ids:
            q = Q(guidebox_data__id=i)

            if self.params:
                self.params = self.params | q

            else:
                self.params = q

        return list(filter(self.filter_by_content_provider, entries))

    def filter_by_content_provider(self, x):
        f = x.channel.filter(self.params)
        if len(f) > 0:
            return False
        else:
            return True


class SportScheduleView(APIView):

    def get(self, request, sport_id):
        s = Sport.objects.get(id=sport_id)

        serializer = ScheduleSerializer(s.schedules.all().latest('date_created'))

        return Response(serializer.data)
