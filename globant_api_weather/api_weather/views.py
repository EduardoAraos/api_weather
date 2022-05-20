from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api_weather.serializers import CityCountrySerializer, ApiWeatherGlobantSerializer
from api_weather.services import (
    api_call_openweathermap,
    api_weather_response,
    now_date_format,
    key_cache_hash)
from django.core.cache import cache


@api_view(['GET'])
def api_weather(request):
    city_country_serializer = CityCountrySerializer(data=request.query_params)
    cached_time = 2 * 60
    request_time = now_date_format()
    if city_country_serializer.is_valid():
        params_city = city_country_serializer.data['city']
        params_country = city_country_serializer.data['country']
        cache_key = "".join([params_city, params_country])
        cache_hash = key_cache_hash(cache_key)
        if cache_hash in cache:
            api_weather_data = cache.get(cache_hash)
        else:
            third_api_call = api_call_openweathermap(
                city=params_city, country=params_country)
            if third_api_call.status_code == 200:
                api_weather_data = api_weather_response(third_api_call.json())
                cache.set(cache_hash, api_weather_data, cached_time)
            else:
                return Response(
                    third_api_call.json(),
                    status=status.HTTP_404_NOT_FOUND)
        api_weather_data["requested_time"] = request_time
        api_weather_serializer = ApiWeatherGlobantSerializer(
            data=api_weather_data)
        if api_weather_serializer.is_valid():
            return Response(data=api_weather_serializer.data)
        else:
            return Response(
                api_weather_serializer.errors,
                status=status.HTTP_409_CONFLICT)
    else:
        return Response(
            city_country_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
