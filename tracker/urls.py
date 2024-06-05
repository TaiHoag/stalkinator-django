from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('tracker/', views.tracker_view, name='tracker_view'),
    path('tracker/data/', views.tracker_data, name='tracker_data'),
    path('geofences/', views.geofence_list, name='geofence_list'),
    path('geofences/add/', views.add_geofence, name='add_geofence'),
    path('geofences/remove/<int:pk>/', views.remove_geofence, name='remove_geofence'),
]
