from select import KQ_FILTER_WRITE
from time import time
from urllib import response
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
# https://openweathermap.org/weathermap?basemap=map&cities=false&layer=radar&lat=30&lon=-20&zoom=3
# https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}

def get_date():
    weekdays = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
    t = date.today()
    week_day = t.weekday()
    day_of_week= weekdays[week_day]

    test = str(t)
    today = int(test[8: 10])
    context = {
        'today':today,
        'week_day':week_day,
        'weekdays':weekdays
    }
    return context
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

def get_weather():
    location= get_location()
    response_weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid=521030405ccbd08fb7f9d42f0860faec")
    data = response_weather.text
    # turn the data into json
    data_json = json.loads(data)
    # weather description
    weather_description = data_json['weather'][0]['description']
    icon = data_json['weather'][0]['icon']
    icon_url = (f'http://openweathermap.org/img/wn/{icon}@2x.png')
    # get the city
    city = data_json['name']
    # temp data
    minTemp = kelvin_to_fahrenheit(data_json['main']['temp_min'])
    temp = kelvin_to_fahrenheit(data_json['main']['temp'])
    maxTemp = kelvin_to_fahrenheit(data_json['main']['temp_max'])
    context= {
        'min':minTemp,
        'temp':temp,
        'max':maxTemp,
        'weather_description':weather_description,
        'icon':icon_url,
        'city':city
    }
    return context

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

    weather = {
        'one': [],
        'two': [],
        'three': [],
        'four': [],
    }

    weather_desc = {
        'one': [],
        'two': [],
        'three': [],
        'four': [],
    }
    # sort through forecast weather descriptions for icons
    for x in box:
        for v in box[x]:
            weather[x].append(v['weather'][0])
    for v in weather:
        for x in weather[v]:
            if x['description'] not in weather_desc[v]:
                weather_desc[v].append(x['description'])
    for y in box:
        for x in box[y]:
            print(x['dt_txt'])

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
    context= {
        'min':temp_min,
        'avg':temp_average,
        'max':temp_max,

    }
    return context


def get_news():
    response = requests.get(
        f'https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json?api-key=WejtFmpOwuiZKQ8d2fAC7tq8hXpaRhV6')
    data = response.text
    json_data = json.loads(data)

    news_titles = {}
    news_abstract = {}
    news_url = {}
    keywords = {}
    for i, x in enumerate(json_data['results']):
        # print(x['title'])
        # print(x['adx_keywords'])
        keywords[i] = [x['adx_keywords']]

        news_titles[i] = x['title']
        news_abstract[i] = x['abstract']
        news_url[i] = x['url']
    # print(keywords[0][0])
    keywords_zero = []
    keywords_zero.append(keywords[0][0])

    # print(keywords_zero)
    return [news_titles, news_abstract, news_url]


def kelvin_to_fahrenheit(x):
    y = round((float(x)-273.15)*(9/5)+32)
    return y

# -----------------------------------------------
def get_map():
    loc = get_location()
    lat = loc['lat']
    lon = loc['lon']
    print(lat, lon)
    # op = 'TA2'
    layer = 'temp_new'
    z = '6'
    # x = f'lat={lat}'
    x = str(lat)
    # y = f'lon={lon}'
    y = str(lon)
    api_key = '521030405ccbd08fb7f9d42f0860faec'
    # https://openweathermap.org/weathermap?basemap=map&cities=false&layer=temperature&lat=30&lon=-20&zoom=3
    url = f'https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={api_key}'
    # url = f"https://tile.openweathermap.org/map/precipitation_new/3/48/-114.3472.png?appid=521030405ccbd08fb7f9d42f0860faec"
    # url = f"http://maps.openweathermap.org/maps/2.0/weather/{op}/{z}/{x}/{y}?appid={api_key}"
    response = requests.get(url)
    print(response)


def img_search(x):
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
    querystring = {"q": "x", "pageNumber": "1",
                   "pageSize": "10", "autoCorrect": "true"}

    headers = {
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "fbf4e82c6emshdd25d05f00e9436p172153jsn2569b320a45d"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    print(response.text)