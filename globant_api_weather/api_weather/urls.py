from django.urls import path
from api_weather import views

urlpatterns = [
    path('weather', views.api_weather),

]
