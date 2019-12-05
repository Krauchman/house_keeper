from rest_framework import serializers
from .models import Measure


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['created', 'power_intake', 'room_id']
