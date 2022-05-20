from rest_framework import serializers


class CityCountrySerializer(serializers.Serializer):
    city = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100)
    country = serializers.CharField(
        required=True, allow_blank=False, max_length=2)


class ApiWeatherGlobantSerializer(serializers.Serializer):
    # Location name
    location_name = serializers.CharField(
        required=True, allow_blank=False, max_length=110)
    # Validate to "ab.cd °F"
    temperature_fahrenheit = serializers.CharField(
        required=True, allow_blank=False, max_length=10)
    # Validate to "ab.cd °C"
    temperature_celsius = serializers.CharField(
        required=True, allow_blank=False, max_length=10)
    # String description =
    wind = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100)
    # String description ?
    cloudiness = serializers.CharField(required=True, allow_blank=False)
    # Validate to "int hpa"
    pressure = serializers.CharField(
        required=True, allow_blank=False, max_length=10)
    # "ab%"
    humidity = serializers.CharField(
        required=True, allow_blank=False, max_length=10)
    # Example "06:07"
    sunrise = serializers.CharField(
        required=True, allow_blank=False, max_length=10)
    # Example "18:00"
    sunset = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=10)
    # Example "[4.61, -74.08]" string
    geo_coordinates = serializers.CharField()
    # Datetime "2018-01-09 11:57:00"
    requested_time = serializers.CharField()
    # Ver que poner
    forecast = serializers.DictField()
