import json
import unittest

from unittest.mock import MagicMock

from hltb_client import HLTBClient


class HLTBClientTests(unittest.TestCase):

    def test_query(self):
        mock = MagicMock()
        mock_response = MagicMock()
        data = self.load_fixture('search.html')
        mock_response.text = data
        mock.post.return_value = mock_response
        result = HLTBClient.query_title('grandia', mock)
        self.assertEqual(str, type(data))
        self.assertEqual(result, data)

    def test_cleanse_times_normal(self):
        time_string = "41 Hours"
        result = HLTBClient.cleanse_times(time_string)
        self.assertEqual(float, type(result))
        self.assertEqual(result, 41.0)

    def test_cleanse_times_half_encoded(self):
        time_string = "32&#189; Hours"
        result = HLTBClient.cleanse_times(time_string)
        self.assertEqual(float, type(result))
        self.assertEqual(result, 32.5)

    def test_cleanse_times_half_unencoded(self):
        time_string = "99½ Hours"
        result = HLTBClient.cleanse_times(time_string)
        self.assertEqual(float, type(result))
        self.assertEqual(result, 99.5)

    def test_cleanse_times_none(self):
        time_string = "--"
        result = HLTBClient.cleanse_times(time_string)
        self.assertEqual(float, type(result))
        self.assertEqual(result, 0.0)

    def test_parse_query(self):
        data = self.load_fixture('search.html')
        result = HLTBClient.parse_query(data)
        expected = json.loads(self.load_fixture('search_results.json'))
        self.assertEqual(list, type(result))
        self.assertEqual(result, expected)

    def test_search(self):
        mock = MagicMock()
        mock_response = MagicMock()
        data = self.load_fixture('search.html')
        expected = json.loads(self.load_fixture('search_results.json'))
        mock_response.text = data
        mock.post.return_value = mock_response
        result = HLTBClient.search('grandia', mock)
        self.assertEqual(list, type(result))
        self.assertEqual(expected, result)

    @staticmethod
    def load_fixture(file):
        with open(f'fixtures/{file}', 'r') as file:
            return file.read()