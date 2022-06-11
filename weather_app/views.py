
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
import requests
import json
from datetime import date

# from weather import weather_app
from .forms import NewUser, LoginUser, SearchWeather
from django.contrib.auth.decorators import login_required
from .funct import *
# Create your views here.
w = get_weather()
icon_url = w['icon']


def index(request):
    test = 'test'
    context = {
        'test': test
    }
    return render(request, 'weather_app/index.html')


def sign_up(request):
    if request.method == "GET":
        form = NewUser()

        context = {
            'icon_url':icon_url,
            'form': form,
        }
        return render(request, 'weather_app/sign_up.html', context)
    elif request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                # first_name= form.cleaned_data['first_name'],
                # last_name= form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            return HttpResponseRedirect(reverse('login_user'))


def login_user(request):
    if request.method == "GET":

        return render(request, 'weather_app/login.html', {
            'form': LoginUser(),
            'icon_url':icon_url,
        })
    elif request.method == "POST":
        form = LoginUser(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(
                request, username=form.cleaned_data['username'], password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))
            else:
                form.add_error('username', 'Invalid Credentials')
                return render(request, 'weather_app/login.html', {
                    'form': form,
                    'icon_url':icon_url,
                })


def logout_user(request):
    logout(request)
    return redirect(reverse('login_user'))


@login_required
def profile(request):

    return render(request, 'weather_app/profile.html', {'icon_url':icon_url,})


@login_required
def edit_profile(request, id):
    user = User.objects.filter(id=id)
    return render(request, 'weather_app/edit.html', {
        'user': user,
        'icon_url':icon_url,
    })


def search(request):
    get_map()
    if request.method == 'GET':
        return render(request, 'weather_app/search.html')
    elif request.method == "POST":
        query = request.POST
        query_search = query['search']
        if len(query_search) != 5:
            err = 'please enter a valid zip code'
            return render(request, 'weather_app/search.html', {'err': err})

        for x in query_search:

            try:
                if int(x) * 0 != 0:
                    pass
            except:
                err = 'please enter a valid zip code'
                return render(request, 'weather_app/search.html', {'err': err})
        query_search = int(query_search)

        try:

            # url = f'https://api.openweathermap.org/data/2.5/weather?zip={query_search},us&appid=521030405ccbd08fb7f9d42f0860faec'
            # response = requests.get(url)
            # data = response.text
            # json_data = json.loads(data)

            # return render(request, 'weather_app/search.html', {'data': json_data})
            results = search_by_zip(query_search)
            description = results[0]
            name = results[1]
            temp = kelvin_to_fahrenheit(int(results[2]))
            temp_min = kelvin_to_fahrenheit(int(results[3]))
            temp_max = kelvin_to_fahrenheit(int(results[4]))
            icon = results[5]
            icon_url = (f'http://openweathermap.org/img/wn/{icon}@2x.png')
            context = {
                'description': description,
                'name': name,
                'temp': temp,
                'temp_min': temp_min,
                'temp_max': temp_max,
                'icon_url': icon_url,
            }
            return render(request, 'weather_app/search.html', context)
        except:
            err = 'please enter a valid zip code'
            return render(request, 'weather_app/search.html', {'err': err})

        # context = {
        #     'query': query['search'],

        # }
        # return render(request, 'weather_app/search.html', context)

# also home
def home(request):
    # get location from ip-api
    location = get_location()
    # get weather for main display
    weather= get_weather()
    minTemp= weather['min']
    temp= weather['temp']
    maxTemp= weather['max']
    weather_description= weather['weather_description']
    icon_url= weather['icon']
    city= weather['city']

    # -----------------------------------------------
    

    news = get_news()
    # print(news[0])
    titles = news[0]
    abstract = news[1]
    abst_zero = abstract[0]
    abst_one = abstract[1]
    abst_two = abstract[2]
    urls = news[2]
    # for i, x in enumerate(titles):
    #     print(i)

    # f_temp= round((float(temp)-273.15) * (9/5) + 32)

    # -----------------------------------------------
    # get date for forecast 
    the_date=get_date()
    today= the_date['today']
    weekday= the_date['week_day']
    # -----------------------------------------------
    # get forecast
    forecast = get_forecast()
    forecast_min = forecast['min']
    forecast_avg = forecast['avg']
    forecast_max = forecast['max']

    context = {
        # current weather and location
        'weather_description': weather_description,
        'min': minTemp,
        'temp': temp,
        'max': maxTemp,
        'city': city,
        'icon_url': icon_url,

        # for the dates for the forecast
        'today': today,
        'weekday': weekday,
        # forecast
        'fore': forecast,
        'min_for': forecast_min,
        'avg_for': forecast_avg,
        'max_for': forecast_max,
        # location
        'lat': location['lat'],
        'lon': location['lon'],
        'titles': titles,
        'abstract': abstract,
        'abst_zero': abst_zero,
        'urls': urls,

    }
    return render(request, 'weather_app/home.html', context)

def forecast(request):

    the_date=get_date()
    today = the_date['today']
    weekday = the_date['week_day']

    forecast = get_forecast()
    forecast_min = forecast['min']
    forecast_avg = forecast['avg']
    forecast_max = forecast['max']


    context = {

        'min':forecast_min,
        'avg':forecast_avg,
        'max':forecast_max,
        'today':today,
        'weekday':weekday,
        'icon_url':icon_url,


    }
    return render(request, 'weather_app/forecast.html',context)






# -----------------------------------------------


def spotify(request):
    CLIENT_ID = '8c4452fc1e6a4b3196c9214e07378883'
    CLIENT_SECRET = '77f704981e9c4b89b83a7b965b31965b'

    def get_token():

        AUTH_URL = 'https://accounts.spotify.com/api/token'

        auth_response = requests.post(AUTH_URL, {

            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        })
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']

        return access_token

    token = get_token()

    def get_track(access_token):

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            # 'Authorization': '{access_token}'.format(access_token=access_token),
            # 'Content-Type': 'application/json'
        }
        print(headers)

        BASE_URL = 'https://api.spotify.com/v1/'
        track_id = '6y0igZArWVi6Iz0rj35c1Y'
        response = requests.get(
            BASE_URL + 'tracks/' + track_id, headers=headers)

        # print(response.json())

        # auth_response_data = auth_response.json()
        # access_token = auth_response_data['access_token']

    context = {
        'token': token,
        'id': CLIENT_ID
    }
    return render(request, 'weather_app/spotify.html', context)


def spotify_login(request):
    CLIENT_ID = '8c4452fc1e6a4b3196c9214e07378883'
    CLIENT_SECRET = '77f704981e9c4b89b83a7b965b31965b'
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    redirect_uri = 'http://127.0.0.1:8000/spotify/'

    url = 'https://accounts.spotify.com/authorize/'

    auth_response = requests.get(url, {

        'client_id': CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scopes': 'user-read-private user-read-email',
    })
    print(auth_response)
    return redirect(reverse('spotify'))


def test(request):
    CLIENT_ID = '8c4452fc1e6a4b3196c9214e07378883'
    redirect_uri = 'http://127.0.0.1:8000/spotify/'

    # response = requests.get('https://accounts.spotify.com/authorize/', {
    #     'client_id': CLIENT_ID,
    #     'scopes': 'user-read-private user-read-email',
    #     'redirect_uri': redirect_uri
    # })
    # print(response)
    # return redirect(reverse('spotify'))
    return HttpResponseRedirect(f'https://accounts.spotify.com/authorize/{CLIENT_ID}', headers={
        'client_id': CLIENT_ID,
        'redirect_uri': redirect_uri
    })
