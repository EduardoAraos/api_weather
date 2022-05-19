import unittest, json

from services import key_cache_hash

class TestKey_cache_hash(unittest.TestCase):
    def test_collisions_amount(self):
        """
        Test that the number of collisions is zero,
        comparing the list of cities to the same list
        but hashed with md5
        """
        hash_set = set()
        with open("static/city_country_list.json") as f:
            data = json.load(f)
            for city_country in data:
                hash_set.add(key_cache_hash(city_country))

            self.assertEqual(len(hash_set), len(data))


if __name__ == '__main__':
    unittest.main()