from django.urls import path
from . import views

app_name = 'forecast'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('autocomplete/', views.city_autocomplete, name='city_autocomplete'),
    path('stats/', views.city_stats, name = 'city_stats'),
]