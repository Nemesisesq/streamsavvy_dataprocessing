from rest_framework import serializers
from data_processor.models import *


class ServiceDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceDescription
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Content
        depth = 2


class ViewingServicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ViewingServices


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        depth = 2


class ModuleDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleDescriptions
        depth = 2
