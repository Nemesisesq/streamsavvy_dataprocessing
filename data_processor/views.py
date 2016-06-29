import json

from django.http import HttpResponse
from django.shortcuts import render
from fuzzywuzzy import fuzz
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from data_processor.guidebox import GuideBox
from data_processor.models import ServiceDescription
from data_processor.serializers import ServiceDescriptionSerializer, ContentSerializer
from rest_framework import viewsets

# Create your views here.

class ServiceDescriptionViewSet(viewsets.ModelViewSet):

    queryset = ServiceDescription.objects.all()
    serializer_class = ServiceDescriptionSerializer
    lookup_field = 'slug'



class SearchContentViewSet(viewsets.ModelViewSet):

    q = ""

    serializer_class = ContentSerializer

    def get_queryset(self):
        self.q = self.request.GET.get('q', '')
        sqs = SearchQuerySet().autocomplete(content_auto=self.q).exclude(title=None)[:10]
        suggestions = [result.object for result in sqs]

        suggestions = list(reversed(sorted(suggestions, key=self.get_ratio)))

        filter_results = self.check_guidebox_for_query(suggestions, self.q)
        # filter_results['search_term'] = self

        filter_results = [x for x in filter_results if x.guidebox_data['id'] not in [3084, 31168, 31150, 15935]]

        # banned server

        filter_results = [show for show in filter_results if show.id != 15296]

        filter_results = [GuideBox().process_content_for_sling_ota_banned_channels(show) for show in filter_results]

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





