import json

from django.http import HttpResponse
from django.shortcuts import render
from fuzzywuzzy import fuzz
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

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

        return suggestions

    def get_ratio(self, obj):
        return fuzz.ratio(self.q, obj.title)





