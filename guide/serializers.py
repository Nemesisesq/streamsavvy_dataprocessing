from rest_framework import serializers

from guide.models import RoviGridSchedule


class RoviGridScheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoviGridSchedule

