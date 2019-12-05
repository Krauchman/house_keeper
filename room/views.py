import json

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Room, Measure
from .serializers import MeasureSerializer


class AddMeasure(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        room_number = data.get('room_number')
        measure_value = data.get('measure_value')

        if None in (room_number, measure_value):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='{"error": "Please provide all the fields"}')

        room = Room.objects.filter(number=room_number)
        if not room:
            return Response(status=status.HTTP_404_NOT_FOUND, data='{"fail": "Room not found"}')
        room = room.first()

        if request.user.id != room.measurer_id:
            return Response(status=status.HTTP_403_FORBIDDEN, data='{"fail": "Not allowed"}')

        room.measure_set.create(power_intake=measure_value)
        measures = room.measure_set.all()
        if len(measures) > settings.NUMBER_OF_MEASURES_PER_ROOM:
            measures.first().delete()

        return Response(status=status.HTTP_200_OK, data='{"ok": "Success"}')


class GetMeasures(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        room_number = data.get('room_number')
        measures_number = data.get('measures_number', 20)

        if room_number is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='{"error": "Please provide all the fields"}')

        room = Room.objects.filter(number=room_number)
        if not room:
            return Response(status=status.HTTP_404_NOT_FOUND, data='{"fail": "Room not found"}')
        room = room.first()

        if request.user not in room.owners:
            return Response(status=status.HTTP_403_FORBIDDEN, data='{"fail": "Not allowed"}')

        measures = room.measure_set.all()
        if len(measures) < measures_number:
            measures_number = len(measures)

        measures = measures[-measures_number:]

        measures_data = {'ok': 'Success', 'measures': [MeasureSerializer(measure).data for measure in measures]}

        return Response(status=status.HTTP_200_OK, data=json.dumps(measures_data))
