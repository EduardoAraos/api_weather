import unittest, json

from services import key_cache_hash, get_dict

class TestKey_cache_hash(unittest.TestCase):
    def test_collisions_amount(self):
        """
        Test that the number of collisions is zero,
        comparing the lenth of list of cities to 
        the same list but hashed with md5
        """
        hash_set = set()
        filename = 'static/city_country_list.json'
        with open(filename) as f:
            data = json.load(f)
            for city_country in data:
                hash_set.add(key_cache_hash(city_country))

            self.assertEqual(len(hash_set), len(data))

class TestGet_dict(unittest.TestCase):
    def test_dict_not_nested(self):
        a_dict = {'a_key': 'a_value'}
        result = get_dict(a_dict, ['a_key'])
        self.assertEqual(result, 'a_value')
    
    def test_dict_nested(self):
        a_dict = {'a_key': {'b_key': 'b_value'}}
        result = get_dict(a_dict, ['a_key', 'b_key'])
        self.assertEqual(result ,'b_value')

    def test_dict_nested_2(self):
        a_dict = {'a_key': 
            {'b_key': 
                {'c_key': 
                    {'d_key': 123}
                }
            }
        }
        result = get_dict(a_dict,['a_key', 'b_key', 'c_key', 'd_key'])
        self.assertEqual(result, 123)
    
    def test_dict_key_error(self):
        a_dict = {'a_key': 23}
        result = get_dict(a_dict, ['some_key'])
        self.assertEqual(result ,'N/A')

if __name__ == '__main__':
    unittest.main()