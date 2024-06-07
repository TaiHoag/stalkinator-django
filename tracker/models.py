from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Geofence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField(default=1000)
    categories = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else f"Geofence at ({self.latitude}, {self.longitude})"
