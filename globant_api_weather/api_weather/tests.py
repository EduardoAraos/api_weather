import unittest
import json
import random

from api_weather.services import (key_cache_hash,
                                  get_dict, cloudiness_description,
                                  wind_description, celsius_to_fahrenheit,)


class Test_key_cache_hash(unittest.TestCase):

    def test_collisions_amount(self):
        """
        Test that the number of collisions is zero,
        comparing the lenth of list of cities to
        the same list but hashed with md5
        """

        hash_set = set()
        filename = './api_weather/static/city_country_list.json'
        with open(filename) as f:
            data = json.load(f)
            for city_country in data:
                hash_set.add(key_cache_hash(city_country))

            self.assertEqual(len(hash_set), len(data))


class Test_get_dict(unittest.TestCase):

    def test_dict_not_nested(self):
        """
        Test for getter of a value with a key
        """
        a_dict = {'a_key': 'a_value'}
        result = get_dict(a_dict, ['a_key'])
        self.assertEqual(result, 'a_value')

    def test_dict_nested(self):
        """
        Test for getter of a nested value with nested keys
        """
        a_dict = {'a_key': {'b_key': 'b_value'}}
        result = get_dict(a_dict, ['a_key', 'b_key'])
        self.assertEqual(result, 'b_value')

    def test_dict_nested_2(self):
        """
        Test for getter of deep nested value with nested keys
        """
        a_dict = {'a_key':
                  {'b_key':
                   {'c_key':
                    {'d_key': 123}
                    }
                   }
                  }
        result = get_dict(a_dict, ['a_key', 'b_key', 'c_key', 'd_key'])
        self.assertEqual(result, 123)

    def test_dict_key_error(self):
        """
        Test for getter with a non existent key
        """
        a_dict = {'a_key': 23}
        result = get_dict(a_dict, ['some_key'])
        self.assertEqual(result, 'N/A')


class Test_cloudiness_description(unittest.TestCase):
    """
    See the classs Test_wind_description docs
    if u want to see the strategy for testing
    these functions
    """

    def test_cloud_clear_only_value(self):
        """
        Test to check that 0% cloud cover is sky clear
        """

        result = cloudiness_description(0)
        self.assertEqual(result, 'Sky clear')

    def test_few_clouds_lower_bound(self):
        """
        Test to check that 0<value<31.25 cloud cover is few clouds
        """

        result = cloudiness_description(.0001)
        self.assertEqual(result, 'Few clouds')

    def test_few_clouds_upper_bound(self):
        """
        Test to check that 0<value<31.25 cloud cover is few clouds
        """

        result = cloudiness_description(18.7499)
        self.assertEqual(result, 'Few clouds')

    def test_cloud_scattered_lower_bound(self):
        """
        Test to check that 31.25<=value<56.25 cloud cover is scattered
        """

        result = cloudiness_description(31.25)
        self.assertEqual(result, 'Scattered')

    def test_cloud_scattered_upper_bound(self):
        """
        Test to check that 31.25<=value<56.25 cloud cover is scattered
        """

        result = cloudiness_description(56.2499)
        self.assertEqual(result, 'Scattered')

    def test_cloud_broken_lower_bound(self):
        """
        Test to check that 56.25<=value<100 cloud cover is scattered
        """

        result = cloudiness_description(56.25)
        self.assertEqual(result, 'Broken')
        pass

    def test_cloud_broken_upper_bound(self):
        """
        Test to check that 56.25<=value<100 cloud cover is scattered
        """

        result = cloudiness_description(99.99)
        self.assertEqual(result, 'Broken')
        pass

    def test_cloud_overcast(self):
        """
        Test to check that a value = 100 means overcast clouds
        """

        result = cloudiness_description(100)
        self.assertEqual(result, 'Overcast')


class Test_wind_description(unittest.TestCase):
    """
    Consider this for the testing strategy
    for this function and cloudiness description :
    x = random.randrange(a, b, epsilon)
    with a<= x < b-epsilon
    could be a good way to test the values in range
    of each wind description, but i value more
    testing edge cases of each range, as you could
    see in wind_description and cloudiness_description
    the lookup tables are monotonically increasing values
    so the binary search used could tell us
    that any value within the edge cases tested
    obey the rule.
    """

    def test_wind_speed_value(self):
        """
        Test to check that the passed to the function
        is the same that is returned
        """
        wind_degrees = random.randint(0, 10**3)
        wind_speed = random.randint(0, 10**3)
        result = wind_description(wind_speed, wind_degrees)[1]
        self.assertEqual(result, wind_speed)

    def test_wind_speed_calm(self):
        """
        Test to check that wind speed of 0 <= value < .5 [m/s]
        is calm description
        """
        # wind speed its full independent
        # from its degrees (direction of wind)
        wind_degrees = random.randint(0, 10**3)
        result = wind_description(.49, wind_degrees)[0]
        self.assertEqual(result, 'Calm')

    def test_wind_speed_light_air(self):
        """
        Test to check that wind speed of 0.5 <= value < 1.6 [m/s]
        is light air description
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(1.59, wind_degrees)[0]
        self.assertEqual(result, 'Light air')

    def test_wind_speed_light_breeze(self):
        """
        Test to check that wind speed of 1.6 <= value < 3.4 [m/s]
        is light breeze description
        """
        wind_degrees = random.randint(0, 10**4)
        result = wind_description(3.39, wind_degrees)[0]
        self.assertEqual(result, 'Light breeze')

    def test_wind_speed_gentle_breeze(self):
        """
        Test to check that wind speed of 3.4 <= value < 5.5 [m/s]
        is gentle breeze
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(5.49, wind_degrees)[0]
        self.assertEqual(result, 'Gentle breeze')

    def test_wind_speed_moderate_breeze(self):
        """
        Test to check that wind speed of 5.5 <= value < 8 [m/s]
        is moderate breeze
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(7.99, wind_degrees)[0]
        self.assertEqual(result, 'Moderate breeze')

    def test_wind_speed_fresh_breeze(self):
        """
        Test to check that wind speed of 8 <= value < 10.8 [m/s]
        is fresh breeze
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(10.79, wind_degrees)[0]
        self.assertEqual(result, 'Fresh breeze')

    def test_wind_speed_strong_breeze(self):
        """
        Test to check that wind speed of 10.8 <= value <= 13.9 [m/s]
        is strong
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(13.8, wind_degrees)[0]
        self.assertEqual(result, 'Strong breeze')

    def test_wind_high_wind(self):
        """
        Test to check that wind speed of 13.9 <= value < 17.2 [m/s]
        is fresh breeze
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(17.19, wind_degrees)[0]
        self.assertEqual(result, 'High wind')

    def test_gale_wind(self):
        """
        Test to check that wind speed of 17.2 <= value < 20.8 [m/s]
        is fresh breeze
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(20.79, wind_degrees)[0]
        self.assertEqual(result, 'Gale')

    def test_strong_gale_wind(self):
        """
        Test to check that wind speed of 20.8 <= value < 24.5 [m/s]
        is gale wind
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(23.49, wind_degrees)[0]
        self.assertEqual(result, 'Strong gale')

    def test_storm_wind_wind(self):
        """
        Test to check that wind speed of 24.5 <= value < 28.5 [m/s]
        is storm wind
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(28.49, wind_degrees)[0]
        self.assertEqual(result, 'Storm')

    def test_violent_storm_wind(self):
        """
        Test to check that wind speed of 28.5 <= value < 32.7 [m/s]
        is storm wind
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(32.69, wind_degrees)[0]
        self.assertEqual(result, 'Violent storm')

    def test_hurricane_force_wind(self):
        """
        Test to check that wind speed of 32.7 <= value < inf [m/s]
        is storm wind
        For practical purposes inf = 10**4, historically
        The highest wind speed ever recorded occurred on
        Barrow Island, Australia. On April 10th, 1996
        an unmanned weather station measured a 253 mph
        wind gust during Tropical Cyclone Olivia.
        253 [Mph] roughly translates to 113 [m/s]
        So we can tell 10**4 >> 113 should be enough
        for practical purposes.
        Tornadoes wind speed exceeds these wind speeds,
        but they are measured behind another scale
        (The Fujita Scale of Tornado Intensity)
        not the used here (The Beaufort scale).
        """
        wind_degrees = random.randint(0, 10**9)
        result = wind_description(-.01 + 10**4, wind_degrees)[0]
        self.assertEqual(result, 'Hurricane force')

    def test_wind_rose_n(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        range 348.75 <= (value%360) < 11.25
        is north
        """
        wind_degrees = 348.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'North')

    def test_wind_rose_nne(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 11.25 <= (value%360) < 33.75
        is north north east
        """
        wind_degrees = 11.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'North-NorthEast')

    def test_wind_rose_ne(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 33.75 <= (value%360) < 56.25
        is north east
        """
        wind_degrees = 33.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'North-East')

    def test_wind_rose_ene(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 56.25 <= (value%360) < 78.75
        is east north east
        """
        wind_degrees = 56.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'East-NorthEast')

    def test_wind_rose_e(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 78.75 <= (value%360) < 101.25
        is east
        """
        wind_degrees = 78.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'East')

    def test_wind_rose_ese(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 101.25 <= (value%360) < 123.75
        is easth south east
        """
        wind_degrees = 101.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'East-SouthEast')

    def test_wind_rose_se(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 123.75 <= (value%360) < 146.25
        is south east
        """
        wind_degrees = 123.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'South-East')

    def test_wind_rose_sse(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 146.25 <= (value%360) < 168.75
        is south south east
        """
        wind_degrees = 146.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'South-SouthEast')

    def test_wind_rose_s(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 168.75 <= (value%360) < 191.25
        is south
        """
        wind_degrees = 168.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'South')

    def test_wind_rose_ssw(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 191.25 <= (value%360) < 213.75
        is south south west
        """
        wind_degrees = 191.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'South-SouthWest')

    def test_wind_rose_sw(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 213.75 <= (value%360) < 236.25
        is south west
        """
        wind_degrees = 213.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'South-West')

    def test_wind_rose_wsw(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 236.25 <= (value%360) < 258.75
        is west south west
        """
        wind_degrees = 236.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'West-SouthWest')

    def test_wind_rose_w(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 258.75 <= (value%360) < 281.25
        is west
        """
        wind_degrees = 258.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'West')

    def test_wind_rose_wnw(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 281.25 <= (value%360) < 303.75
        is west north west
        """
        wind_degrees = 281.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'West-NorthWest')

    def test_wind_rose_nw(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 303.75 <= (value%360) < 326.25
        is north west
        """
        wind_degrees = 303.75 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'North-West')

    def test_wind_rose_nnw(self):
        """
        Test to check that the direction of
        a wind degrees whose values in
        the range 326.25 <= (value%360) < 348.75
        is north north west
        """
        wind_degrees = 326.25 + random.randint(0, 100) * 360
        wind_speed = random.randint(0, 10**2)
        result = wind_description(wind_speed, wind_degrees)[2]
        self.assertEqual(result, 'North-NorthWest')


class Test_celsus_to_fahrenheit(unittest.TestCase):

    def test_absolute_zero(self):
        result = celsius_to_fahrenheit(-273.15)
        self.assertAlmostEqual(result, -459.67, 2)

    def test_boiling_water(self):
        result = celsius_to_fahrenheit(100)
        self.assertAlmostEqual(result, 212)

    def test_freeze_water(self):
        result = celsius_to_fahrenheit(0)
        self.assertAlmostEqual(result, 32)


class Test_now_date_format(unittest.TestCase):
    pass


class Test_unix_time_to_datetime_format(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
