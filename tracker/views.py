from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration
import datetime
import folium
from django.conf import settings
from plyer import notification
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .forms import SignUpForm, GeofenceForm
from .models import Geofence

def home(request):
    if request.user.is_authenticated:
        return redirect('tracker_view')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('tracker_view')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tracker_view')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def tracker_view(request):
    api = get_token()
    last_value = get_tracker_location_data(api)
    lat, lon, points, close_places, map_url = geoapify(last_value, request.user)
    now = datetime.datetime.now()

    context = {
        'lat': lat,
        'lon': lon,
        'update_time': now,
        'close_places': close_places,
        'map_url': map_url
    }
    return render(request, 'tracker/tracker.html', context)

@login_required
def geofence_list(request):
    geofences = Geofence.objects.filter(user=request.user)
    return render(request, 'tracker/geofence_list.html', {'geofences': geofences})

@login_required
def add_geofence(request):
    if request.method == 'POST':
        form = GeofenceForm(request.POST)
        if form.is_valid():
            geofence = form.save(commit=False)
            geofence.user = request.user
            geofence.save()
            return redirect('geofence_list')
    else:
        form = GeofenceForm()
    return render(request, 'tracker/add_geofence.html', {'form': form})

@login_required
def remove_geofence(request, pk):
    geofence = Geofence.objects.get(pk=pk, user=request.user)
    if geofence:
        geofence.delete()
    return redirect('geofence_list')

def tracker_data(request):
    api = get_token()
    last_value = get_tracker_location_data(api)
    lat, lon, points, close_places, map_url = geoapify(last_value, request.user)
    now = datetime.datetime.now()

    data = {
        'lat': lat,
        'lon': lon,
        'update_time': now,
        'close_places': close_places,
        'map_url': map_url
    }

    return JsonResponse(data)


def get_token():
    client_id = "ycJbMxjaptO0kOweZop4v5R6nBsD1i5K"
    client_secret = "r20qXrMRDN53E27LTWsRc3GfSPR7byBhcpgZ7ZVga5LpwZMKK9VCkz8HLS8KXrGP"

    oauth_client = BackendApplicationClient(client_id=client_id)
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"

    oauth = OAuth2Session(client=oauth_client)
    token = oauth.fetch_token(
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )

    access_token = token.get("access_token")

    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)

    api = iot.PropertiesV2Api(client)
    
    return api

def get_tracker_location_data(api):
    thing_id = "ec52da50-685d-4a38-ba5f-fc94716fdf9c"
    try:
        properties = api.properties_v2_list(thing_id)
        for prop in properties:
            if prop.name == "Gps":
                last_value = prop.last_value
                print(last_value)
                return last_value
    except ApiException as e:
        print("Got an exception: {}".format(e))

def geoapify(last_value, user):
    lat = last_value['lat']
    lon = last_value['lon']
    API_KEY = "cd89b5f6cefc4b9ebf4f94117e19577e"

    # Fetch user's geofences and categories
    geofences = Geofence.objects.filter(user=user)
    categories = set()
    for geofence in geofences:
        if geofence.categories:
            categories.update(geofence.categories.split(','))

    categories = ",".join(categories)

    url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},5000&bias=proximity:{lon},{lat}&limit=500&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    points = [(lon, lat)]
    close_places = []

    if 'features' in data:
        for place in data['features']:
            properties = place['properties']
            name = properties.get('name', 'N/A')
            distance = properties.get('distance', 'N/A')
            points.append((properties['lon'], properties['lat']))
            if distance < 5:
                close_places.append(name)
                send_notification(name)

    map_url = generate_map(lat, lon, points)
    return lat, lon, points, close_places, map_url

def generate_map(lat, lon, points):
    map = folium.Map(location=[lat, lon], zoom_start=17)

    # Add the main point
    folium.Marker([lat, lon], popup='Current Location', icon=folium.Icon(color='red')).add_to(map)

    # Add the nearby points
    for pt in points[1:]:
        folium.Marker([pt[1], pt[0]], icon=folium.Icon(color='blue')).add_to(map)

    map_path = os.path.join(settings.BASE_DIR, 'static/maps/map.html')
    map.save(map_path)

    return '/static/maps/map.html'

def send_notification(place_name):
    notification.notify(
        title='Proximity Alert',
        message=f'You are within 5 meters of {place_name}.',
        app_name='Geoapify Tracker'
    )
