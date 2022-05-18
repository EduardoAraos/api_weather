from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api_weather.serializers import CityCountrySerializer, ApiWeatherGlobantSerializer
from api_weather.services import api_call_openweathermap, api_weather_response

@api_view(['GET'])
def api_weather(request):
    city_country_serializer = CityCountrySerializer(data=request.query_params)
    if city_country_serializer.is_valid():
        third_api_data = api_call_openweathermap(city=city_country_serializer.data['city'], country=city_country_serializer.data['country'])
        api_weather_data = api_weather_response(third_api_data)
        api_weather_serializer = ApiWeatherGlobantSerializer(data= api_weather_data)
        if api_weather_serializer.is_valid():
            return Response(data=api_weather_serializer.data)
        else:
            return Response(api_weather_serializer.errors, status=status.HTTP_409_CONFLICT)                    
    else:
        return Response(city_country_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


