from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .models import City, SearchHistory
from django.db.models import F
import json

def get_weather_data(city_name):
    """Получение данных о погоде с API"""
    #Координаты
    #Создаём get запрос на получение данных о городе (координаты)
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
    geo_responce = requests.get(geocoding_url)
    geo_data = geo_responce.json()
    
    if not geo_data.get('results'):
        return None

    city_data = geo_data['results'][0]
    lat = city_data['latitude']
    lon = city_data['longitude']
    
    # выше получаем координаты города
    # дальше получаем данные о  самой погодеe
    
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m&hourly=temperature_2m,precipitation_probability,wind_speed_10m&forecast_days=1"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    
    results = {
        'city_name': city_data.get('name'),
        'country': city_data.get('country'),
        'current': weather_data.get('current', {}),
        'hourly': weather_data.get('hourly', {}),
        'hourly_units': weather_data.get('hourly_units', {})
    }
    
    return results
    
def index(request):
    """"-получение формы поиска погоды"""
    weather_data = None
    city_name = request.GET.get('city', '')    
    search_history = []
    
    if city_name:
        weather_data = get_weather_data(city_name)
        if weather_data:
            city, created = City.objects.get_or_create(name=weather_data['city_name'])
            city.search_count = F('search_count') + 1
            city.save()
        
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
                
            SearchHistory.objects.create(
                city = city,
                user = request.user if request.user.is_authenticated else None,
                session_key = session_key
            )
            
            # Сохраняем последний город в сессии
            request.session['last_city'] = city_name
    #Получчение последнего горда из сессии
    last_city = request.session.get('last_city', '')
    
    #Получения истории поиска текущего пользователя
    session_key = request.session.session_key
    if session_key:
        if request.user.is_authenticated:
            search_history = SearchHistory.objects.filter(
                user = request.user
            ).select_related('city').order_by('-search_time')[:5]
            
    context = {
        'weather_data': weather_data,
        'city_name': city_name,
        'last_city': last_city,
        'search_history':  search_history
    }
    
    return render(request, 'forecast/index.html', context)

def city_autocomplete(request):
    "Подсказки"
    query = request.GET.get('term', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    #Использование API для автодопленнеия
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=5&language=ru&format=json"
    response = requests.get(url)
    data = response.json()
    
    cities = []
    if data.get('results'):
        for city in data['results']:
            city_name = city.get('name', '')
            country = city.get('country', '')
            cities.append(f"{city_name}, {country}")
            
    return JsonResponse(cities, safe=False)

def city_stats(request):
    """"API для статистики поиска"""
    top_cities = City.objects.order_by('-search_count')[:10]
    data = [{'city': city.name, 'count': city.search_count} for city in top_cities]
    return JsonResponse(data, safe=False)