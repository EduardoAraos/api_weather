import requests, datetime, bisect

def api_call_openweathermap(city, country):
    api_key_openweather = '21056e88589f13ccd2c21c8f9acbba8e'
    lang = 'en'
    units_system = 'metric'
    params = {}
    params["q"] = f"{city},{country}"
    params["APPID"] = api_key_openweather
    params["lang"] = lang
    params["units"] = units_system
    url_request = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url_request, params=params)
    print(response)
    # .json() desearilizes json
    return response.json()

def api_weather_response(openweathermap_res):
    location_name = f"{openweathermap_res['name']}, {openweathermap_res['sys']['country']}"
    temperature_fahrenheit = f"{celsius_to_fahrenheit(openweathermap_res['main']['temp']):.2f} °F"
    temperature_celsius = f"{openweathermap_res['main']['temp']} °C"
    wind = wind_description(openweathermap_res['wind']['speed'], openweathermap_res["wind"]["deg"])
    cloudiness = cloudiness_description(openweathermap_res["clouds"]["all"])
    pressure = f"{openweathermap_res['main']['pressure']} hpa"
    humidity = f"{openweathermap_res['main']['humidity']} %"
    sunrise =  unix_time_to_datetime_format(openweathermap_res["sys"]["sunrise"], "%H:%M")
    sunset = unix_time_to_datetime_format(openweathermap_res["sys"]["sunset"], "%H:%M")
    geo_coordinates = f"[{openweathermap_res['coord']['lat']}, {openweathermap_res['coord']['lon']}]"
    requested_time = "N/A"
    forecast =  "N/A"
    response_data = {
        "location_name": location_name,
        "temperature_fahrenheit": temperature_fahrenheit,
        "temperature_celsius": temperature_celsius,
        "wind": wind,
        "cloudiness": cloudiness,
        "pressure": pressure,
        "humidity": humidity,
        "sunrise": sunrise,
        "sunset": sunset,
        "geo_coordinates": geo_coordinates,
        "requested_time" : requested_time,
        "forecast": forecast}
    return response_data


def unix_time_to_datetime_format(utc_time, date_format):
    dt_utc_tz = datetime.datetime.fromtimestamp(utc_time, datetime.timezone.utc)
    return dt_utc_tz.strftime(date_format)

def celsius_to_fahrenheit(celsius_degrees):
    return (celsius_degrees *1.8) + 32

def wind_description(wind_speed=5, wind_degrees=1):
    wind_beaufort_table = [
        (0, 0),
        (.5, 1),
        (1.6, 2),
        (3.4, 3),
        (5.5, 4),
        (8, 5),
        (10.8, 6),
        (13.9, 7),
        (17.2, 8),
        (20.8, 9),
        (24.5, 10),
        (28.5, 11),
        (32.7, 12),
        (10**3, 13)
    ]
    wind_beaufort_description = {
        0:"Calm",
        1:"Light air",
        2:"Light breeze",
        3:"Gentle breeze",
        4:"Moderate breeze",
        5:"Fresh breeze",
        6:"Strong breeze",
        7:"High wind",
        8:"Gale",
        9:"Strong gale",
        10:"Storm",
        11:"Violent storm",
        12:"Hurricane force",
    }
    pos = bisect.bisect_left(wind_beaufort_table, (wind_speed,))
    if wind_speed != 0 and wind_beaufort_table[pos][0] != wind_speed :
        pos-=1
    wind_speed_description = wind_beaufort_description[pos]
    wind_degrees_truncated = int((wind_degrees/22.5)+.5)
    wind_rose_list = [
        'N',
        'NNE',
        'NE',
        'ENE',
        'E',
        'ESE',
        'SE',
        'SSE',
        'S',
        'SSW',
        'SW',
        'WSW',
        'W',
        'WNW',
        'NW',
        'NNW']
    wind_rose_description_dict = {
        'N': "North",
        'NNE': "North-NorthEast",
        'NE': "North-East",
        'ENE': "East-NorthEast",
        'E': "East",
        'ESE': "East-SouthEast",
        'SE': "South-East",
        'SSE': "South-SouthEast",
        'S': "South",
        'SSW': "South-SouthWest",
        'SW': "South-West",
        'WSW': "West-SouthWest",
        'W': "West",
        'WNW': "West-NorthWest",
        'NW': "North-NorthWest",
        'NNW': "North-NorthWest",
    }
    wind_rose_direction =  wind_rose_list[(wind_degrees_truncated % 16)]
    wind_rose_description = wind_rose_description_dict[wind_rose_direction]
    print(wind_speed_description)
    return ", ".join([wind_speed_description, str(wind_speed)+" m/s", wind_rose_description])

def cloudiness_description(cloud_cover_percentage):
    cloudiness_okta_table = [
        (0, 0),
        (18.75, 1),
        (31.25, 2),
        (43.75, 3),
        (56.25, 4),
        (68.75, 5),
        (81.25, 6),
        (100, 7),
        (100+.1,8)
    ]
    cloudiness_okta_description = {
        0:"Sky clear",
        1:"Few clouds",
        2:"Few clouds",
        3:"Scattered",
        4:"Scattered",
        5:"Broken",
        6:"Broken",
        7:"Broken",
        8:"Overcast"
    }
    pos = bisect.bisect_left(cloudiness_okta_table, (cloud_cover_percentage,))
    if cloud_cover_percentage != 0 and cloudiness_okta_table[pos][0] == cloud_cover_percentage:
        pos+=1
    return cloudiness_okta_description[pos]
