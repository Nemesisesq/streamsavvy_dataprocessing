import json

from django.http import HttpResponse
from django.shortcuts import render
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

    serializer_class = ContentSerializer

    def get_queryset(self):
        sqs = SearchQuerySet().autocomplete(content_auto=self.request.GET.get('q', '')).exclude(title=None)[:10]
        suggestions = [result.object for result in sqs]

        return suggestions



# class HaystackSearchView(SearchView):
#
#     def get_queryset(self):
#         queryset = super(HaystackSearchView, self).get_queryset()
#         # further filter queryset based on some set of criteria
#         return queryset.filter(title=self.request.GET['q'])
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(HaystackSearchView, self).get_context_data(*args, **kwargs)
#         # do something
#         return context

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.object for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
