import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from fuzzywuzzy import fuzz, process
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from data_processor.constants import unwanted_show_ids
from data_processor.guidebox import GuideBox
from data_processor.models import ServiceDescription, Channel, Content, ViewingServices, ModuleDescriptions
from data_processor.serializers import ServiceDescriptionSerializer, ContentSerializer, ChannelSerializer, \
    ViewingServicesSerializer, ModuleDescriptionSerializer, SportSerializer
from rest_framework import viewsets


# Create your views here.

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

        res = process.extract(q,w, limit=1)

        t = [ViewingServices.objects.get(name=res[0][0])]



        return t









class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_object(self):
        obj = super(ContentViewSet, self).get_object()

        obj = GuideBox().process_content_for_sling_ota_banned_channels(obj)

        return obj


class SearchSportsViewSet(viewsets.ModelViewSet):
    q = ""

    serializer_class = SportSerializer


    def get_queryset(self):
        self.q = self.request.GET.get('q', '')
        sqs = SearchQuerySet().autocomplete(team_auto=self.q)[:20]

        suggestions = [result.object for result in sqs]

        return suggestions

class SearchContentViewSet(viewsets.ModelViewSet):
    q = ""
    serializer_class = ContentSerializer


    def get_queryset(self):
        self.q = self.request.GET.get('q', '')
        sqs = SearchQuerySet().autocomplete(content_auto=self.q)
        # sqs_sports = SearchQuerySet().autocomplete(team_auto=self.q)[:10]

        print("Search returned")
        suggestions = [result.object for result in sqs]
        filter_results = suggestions
        # suggestions = list(reversed(sorted(suggestions, key=self.get_ratio)))

        filter_results = self.check_guidebox_for_query(suggestions, self.q)
        # filter_results['search_term'] = self

        filter_results = [x for x in filter_results if x.guidebox_data['id'] not in unwanted_show_ids]

        # banned server

        filter_results = [show for show in filter_results if show.id != 15296]

        # filter_results = [GuideBox().process_content_for_sling_ota_banned_channels(show) for show in filter_results]
        print("results sent off")
        return filter_results

    def get_ratio(self, obj):
        return fuzz.ratio(self.q, obj.title)

    def check_guidebox_for_query(self, filter_results, query_string):
        if len(filter_results) == 0:
            g = GuideBox()

            if ('q' in self.request.GET) and self.request.GET['q'].strip():
                result = g.get_show_by_title(query_string)

                result = result['results']

                result_list = []

                for show in result:
                    result_list.append(g.save_content(show))

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
