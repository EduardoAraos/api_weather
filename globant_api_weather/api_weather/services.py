import requests, datetime, bisect, hashlib

def api_call_openweathermap(city, country):
    """Makes an api call to the third app openweathermap api

    Parameters
    ----------
    city : Str
        The speed of wind
    country: Str
        The

    Returns
    -------
    Response object
        The response of the openweathermap api called
    """
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
    # .json() desearilizes json
    return response

def api_weather_response(openweathermap_res):
    """Creates the object response for api_weather api

    Receives the deserialized response from the third app openweathermap api
    and constructs the object that will be the response for the weather api

    Parameters
    ----------
    openmapweathermap_res : dict
        A deserialized json into a python dictionary object that 
        contains the response from the get call at openweathermap api

    Returns
    -------
    Response type object
        The response of the openweathermap api called
    """
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
        "forecast": forecast}
    return response_data


def unix_time_to_datetime_format(utc_time, date_format):
    """Takes a posix timestamp and a format in which it should be represented

    Parameters
    ----------
    utc_time : num
        A posix timestamp
    date_format: str
        A string that represents how the string format of a datetime object
    Returns
    -------
    str
        A human readable string of a date
    """
    dt_utc_tz = datetime.datetime.fromtimestamp(utc_time, datetime.timezone.utc)
    return dt_utc_tz.strftime(date_format)

def celsius_to_fahrenheit(celsius_degrees):
    """Transform celsius unit degrees into fahrenheit unit degrees

    Parameters
    ----------
    celsius_degrees : num
        The amount of celsius degrees

    Returns
    -------
    num
        The equivalence in fahrenheit unit
    """

    return (celsius_degrees *1.8) + 32

def wind_description(wind_speed , wind_degrees):
    """Transform the numeric values of wind speed and wind degrees into a human readable description

    Parameters
    ----------
    wind_speed : Num
        The speed of wind
    wind_degrees: Num
        The degrees of wind

    Returns
    -------
    str
        a human readable description of the wind
    """

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
    return ", ".join([wind_speed_description, str(wind_speed)+" m/s", wind_rose_description])

def cloudiness_description(cloud_cover_percentage):
    """Transform a cloud cover percentage into a human readable description

    Parameters
    ----------
    cloud_cover_percentage : Num
        The percentage of the sky that is cover by clouds

    Returns
    -------
    num
        A human readable description of hows the sky is cover by clouds
    """
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

def now_date_format():
    """Returns the current datetime formatted into a human readable string

    Returns
    -------
    str
        The date of the moment the function is called (E.g. 2022-01-18 22:05:59)
    """
    now_date = datetime.datetime.utcnow()
    return now_date.strftime("%Y-%d-%m %H:%M:%S")

def key_cache_hash(key_prefix):
    """Transforms a string into a md5 hash string representation

    Parameters
    ----------
    key_prefix : str
        A string

    Returns
    -------
    str
        A string hashed into a md5 value
    """
    return hashlib.md5(key_prefix.encode('utf-8')).hexdigest()
