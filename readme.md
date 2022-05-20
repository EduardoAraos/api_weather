# API Weather

Api weather is an api that delivers the current weather given a city and a country, including data such as humidity, pressure, temperature, cloudiness, windness, etc.
## Installation

* Clone the repository

```
$ https://github.com/EduardoAraos/api_weather.git 
$ cd globant_api_weather/ # move to the root src
```

* Create the image for our container
```
$ sudo docker-compose build # sudo is not required if docker is well configured on the machine
```

* Run the application
```
$ sudo docker-compose up # make sure port 8000 before running the app
```
```
...
globant_weather_api_1  | Starting development server at http://0.0.0.0:8000/
...
```
* Run the tests set
```
$ sudo docker-compose run globant_weather_api sh -c "python manage.py test"
```
```
Creating globant_api_weather_globant_weather_api_run ... done
Found 46 test(s).
System check identified no issues (0 silenced).
..............................................
----------------------------------------------------------------------
Ran 46 tests in 0.181s

OK
```
* Try the api!
```
http http://0.0.0.0:8000/weather city=="San Miguel de tucuman" country==AR # you could use curl, postman, etc.
```
```
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Content-Length: 357
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 20 May 2022 10:00:34 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.10
Vary: Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "cloudiness": "Few clouds",
    "forecast": "N/A",
    "geo_coordinates": "[-26.8241, -65.2226]",
    "humidity": "80 %",
    "location_name": "San Miguel de Tucumán,AR",
    "pressure": "1015 hpa",
    "requested_time": "2022-20-05 10:00:33",
    "sunrise": "10:55",
    "sunset": "21:39",
    "temperature_celsius": "8.20 °C",
    "temperature_fahrenheit": "46.76 °F",
    "wind": "Light air, 1.2 m/s, West-NorthWest"
}

```




## Usage



```
$ http http://0.0.0.0:8000/weather city==Bogota country==CO
```
```
...
HTTP/1.1 200 OK
Content-Type: application/json
...
{
    "cloudiness": "Broken",
    "forecast": "N/A",
    "geo_coordinates": "[4.6097, -74.0817]",
    "humidity": "87 %",
    "location_name": "Bogota,CO",
    "pressure": "1027 hpa",
    "requested_time": "2022-20-05 09:17:46",
    "sunrise": "10:42",
    "sunset": "23:03",
    "temperature_celsius": "10.73 °C",
    "temperature_fahrenheit": "51.31 °F",
    "wind": "Light breeze, 3.09 m/s, East-NorthEast"
}
```

### Notes & general developer considerations

**1.** Usually when managing a django application you have to make migrations and migrate them
(create SQL sentences that translate your models from your applications into the database thats configurated).

In this case there is no need to keep register of any models, actually it is, but via cache memory, this
cache memory is configurated to use fast memory (memory ram). So in this case there is no need
to make migrations and migrate them (no use of Django ORM atm).

**2.** The parameters of GET /weather API are city and country, and we should expect that they form a primary key to identify
the city and its country for which we are consulting its weather, well, they are not, in fact the documentation for the
third app <https://openweathermap.org/current#cityid> , tell us that to get unambigous data you should use city id.

The list of the city id for all pairs of cities & countries have around 200.000 pairs, after some data cleaning
theres around 170.000 pairs of unique city & country, there could be many reasons for this behavior, for example every country administrates its own territory organization, for example in the United States they have states and here in Chile we have communes,
this lack of standard could lead to the inconsistent dataset. 

Anyway, dont let this discourage you,the endpoint works just fine with the most well 
known cities of the world, and pretty much all cities of Argentina.

**2.5** Due to the lack of standards mentioned above, the caching strategy sees the pair Córdoba,AR =/= Cordoba,AR and has to cache both options separately. 

**3.** Normally when operating a production level application (independent of its framework i.e.: Django, rails, Spring, ExpressJs, etc)
the environment variables and secrets are securely stored (cryptographically speaking) under a cloud provider of the resource, or at least not shared via the github public repository. 

In this case there are two potential sensitive variables stored in this project:
DJANGO_SECRET and API_KEY_OPW, the first one it is used to sign hash functions on python (for example the key for the cache uses md5 hashing) and the second one is the api key
that the third app provider give us to make requests, given that there is no sensitive data in the application & the api key is totally free
& we are not delivering an application for production, we can afford to share this variables to the world at the moment.

### Todo:
- [ ] Custom validators for the serializers using regular expressions that matches the output data for each value of the response of the GET /weather API.
- [ ] High level documentation interface like swagger, corepi.
- [ ] Factorize the unit tests.
- [ ] Integration tests using mocks.
- [ ] Standard schema for 400 level status code responses of the GET /weather API.
- [ ] Decouple some functionalities to encapsulate better some behaviors, especially the ones that make it difficult to meet the PEP8 standard of lines limited to 79 characters.
- [ ] It could be useful to pass timezone as a parameter into the GET /weather API endpoint so the datetimes.
	  in the response are aware of the timezone, actually all datetimes are in UTC timezone.
- [ ] Forecast for a weekly basis or atleast various days is not available on the third api requesteds, investigate for options.


### Done ✓

- [x] Create readme.md of the project with start up instructions, notes and consiredations of the development and a todo list.
- [x] Development of the application on a public repository on a git based version system.
- [x] Create GET /weather endpoint that takes city and country as parameters.
- [x] Fully build the response object required (except for forecast key).
- [x] Requested weather map from third app provider.
- [x] Response is human readable.
- [x] Keep a cache of 2 minutes for the data requested.
- [x] Low level functions tested.
- [x] Development of all core functionality.

### Why you made this?
This is part of a technical challenge for Globant