# Register your models here.
from django.contrib import admin
from .models import Profile, Geofence

# Register Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Customize the display fields if needed
    list_display = ['user']

# Register Geofence model
@admin.register(Geofence)
class GeofenceAdmin(admin.ModelAdmin):
    # Customize the display fields if needed
    list_display = ['name', 'latitude', 'longitude', 'radius']