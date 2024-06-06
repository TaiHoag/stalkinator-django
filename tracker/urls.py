from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tracker/', views.tracker_view, name='tracker_view'),
    path('tracker/data/', views.tracker_data, name='tracker_data'),
    path('geofences/', views.geofence_list, name='geofence_list'),
    path('geofences/add/', views.add_geofence, name='add_geofence'),
    path('geofences/remove/<int:pk>/', views.remove_geofence, name='remove_geofence'),
]
