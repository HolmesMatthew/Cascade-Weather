from time import time
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
import requests
import json
from datetime import date
from .forms import NewUser, LoginUser
from django.contrib.auth.decorators import login_required

# -----------------------------------------------


def search_by_zip(query_search):
    url = f'https://api.openweathermap.org/data/2.5/weather?zip={query_search},us&appid=521030405ccbd08fb7f9d42f0860faec'
    response = requests.get(url)
    data = response.text
    json_data = json.loads(data)
    weather = json_data['weather'][0]['description']
    name = json_data['name']
    main = json_data['main']
    temp = main['temp']
    min_temp = main['temp_min']
    max_temp = main['temp_max']
    icon = json_data['weather'][0]['icon']

    return [weather, name, temp, min_temp, max_temp, icon]


def get_location():
    response_location = requests.get('http://ip-api.com/json')
    data_ip = response_location.text
    parsed_data = json.loads(data_ip)
    lat = parsed_data['lat']
    lon = parsed_data['lon']
    return {'lat': lat, 'lon': lon}


def get_forecast():
    location = get_location()
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={location["lat"]}&lon={location["lon"]}&appid=521030405ccbd08fb7f9d42f0860faec')
    data = response.text
    json_data = json.loads(data)
    # print(json_data['list'])
    # print(json_data['list'][0]['dt_txt'][0:10])
    box = {
        'one': [],
        'two': [],
        'three': [],
        'four': [],
    }
    # return json_data
    # sort through forecast data
    for index, value in enumerate(json_data['list']):

        # print(value, 'this is value')

        day_value = value['dt_txt'][8:10]
        t = date.today()
        test = str(t)
        if int(test[8:10]) == 31:
            today = int(test[9:10])
        elif int(test[8:9]) == 0:
            today = int(test[9:10])
        else:
            today = int(test[8:10])

        if int(day_value) == today+1:
            # print(f'{today} and {day_value} match')
            box['one'].append(value)
        elif int(day_value) == today+2:
            box['two'].append(value)
        elif int(day_value) == today+3:
            box['three'].append(value)
        elif int(day_value) == today+4:
            box['four'].append(value)
    # print(box)
    temp_min = []
    temp_average = []
    temp_max = []

    # print(box)

    # get min
    for x in box:
        all_temp = []
        for i in box[x]:
            all_temp.append(i['main']['temp_min'])

        temp_min.append(kelvin_to_fahrenheit(min(all_temp)))
    # get average
    for x in box:
        all_temp = 0
        for t in box[x]:
            all_temp += t['main']['temp']
        temp_average.append(kelvin_to_fahrenheit(all_temp/len(box[x])))
    # get max
    for x in box:
        all_temp = []
        for i in box[x]:
            all_temp.append(i['main']['temp_max'])

        temp_max.append(kelvin_to_fahrenheit(max(all_temp)))

    return [temp_min, temp_average, temp_max]


def get_news():
    location = get_location()
    response = requests.get(
        f'https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json?api-key=WejtFmpOwuiZKQ8d2fAC7tq8hXpaRhV6')
    data = response.text
    json_data = json.loads(data)

    news_titles = {}
    news_abstract = {}
    news_url = {}

    for i, x in enumerate(json_data['results']):
        # print(x['title'])
        news_titles[i] = x['title']
        news_abstract[i] = x['abstract']
        news_url[i] = x['url']
    return [news_titles, news_abstract, news_url]


def kelvin_to_fahrenheit(x):
    y = round((float(x)-273.15)*(9/5)+32)
    return y

# -----------------------------------------------