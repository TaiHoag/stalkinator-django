from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Geofence

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class GeofenceForm(forms.ModelForm):
    categories = forms.CharField(help_text="Enter categories separated by commas (e.g., catering.pub, accommodation.hotel)")
    class Meta:
        model = Geofence
        fields = ['name', 'latitude', 'longitude', 'radius', 'categories']