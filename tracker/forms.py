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
    CATEGORY_CHOICES = [
        ('catering.pub', 'Pub'),
        ('accommodation.hotel', 'Hotel'),
        ('commercial.smoking', 'Smoking Area'),
        ('adult.nightclub', 'Nightclub'),
        ('commercial.erotic', 'Erotic Services'),
        ('accommodation.hotel', 'Hotel'),
        ('catering.bar', 'Bar'),
        ('adult', 'Adult Services'),
        # Add more categories as needed
    ]

    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.SelectMultiple(),
        help_text="Select categories"
    )
    location_name = forms.CharField(
        required=False,
        help_text="Enter a location name to search for its coordinates"
    )
    is_allowed = forms.BooleanField(required=False, help_text="Notify when entering or exiting this place")
    is_prohibited = forms.BooleanField(required=False, help_text="Notify when being nearby this place")

    class Meta:
        model = Geofence
        fields = ['name', 'latitude', 'longitude', 'radius', 'categories', 'location_name', 'is_allowed', 'is_prohibited']

    def __init__(self, *args, **kwargs):
        super(GeofenceForm, self).__init__(*args, **kwargs)
        self.fields['categories'].required = False
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False
        self.fields['location_name'].required = False
        self.fields['is_allowed'].required = False
        self.fields['is_prohibited'].required = False