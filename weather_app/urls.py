"""weather_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('edit/<int:id>', views.edit_profile, name='edit'),
    path('forecast/', views.forecast, name='forecast'),
    
    # 
    path('test/', views.test, name='test'),
    path("spotify/", views.spotify, name='spotify'),
    path("spotify-login/", views.spotify_login, name='spotify-login')

]
