from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    is_empty = models.BooleanField(default=True)

    owners = models.ManyToManyField(User, related_name='owned_rooms')
    measurer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='measured_rooms')

    def __str__(self):
        return self.number


class Measure(models.Model):
    class Meta:
        ordering = ['created']

    power_intake = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room) + '-' + str(self.created) + '-' + str(self.power_intake)
