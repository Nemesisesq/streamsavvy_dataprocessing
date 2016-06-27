from rest_framework import serializers
from data_processor.models import *


class ServiceDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:

        model = ServiceDescription
        lookup_field =  'slug'
        extra_kwargs= {
            'url' : {'lookup_field': 'slug'}
        }

class ContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Content
