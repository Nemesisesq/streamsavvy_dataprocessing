from rest_framework import serializers
from data_processor.models import *


class ServiceDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceDescription
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule


class SportSerializer(serializers.ModelSerializer):
    schedules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sport
        depth = 2


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Content
        depth = 2


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('title', 'curr_pop_score', 'guidebox_data')


class ViewingServicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ViewingServices


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        depth = 2


class ModuleDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModuleDescriptions
        depth = 2
