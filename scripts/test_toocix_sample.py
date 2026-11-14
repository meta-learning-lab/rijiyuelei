import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import toocix_sample as sample


class SampleTests(unittest.TestCase):
    @patch('toocix_sample.time.sleep')
    def test_pagination_keeps_distinct_exact_readings(self, _sleep):
        def get(url):
            if 'offset=0' in url:
                return {'total': 31, 'items': [{'id': 1, 'term': '奔'}, {'id': 9, 'term': '奔跑'}]}
            if 'offset=30' in url:
                return {'total': 31, 'items': [{'id': 2, 'term': '奔'}]}
            return {'id': int(url.rsplit('/', 1)[1]), 'term': '奔', 'senses': []}

        result = sample.lookup('奔', max_pages=2, getter=get)
        self.assertEqual([entry['id'] for entry in result['entries']], [1, 2])
        self.assertTrue(result['search_complete'])

    @patch('toocix_sample.time.sleep')
    def test_truncated_search_is_not_reported_complete(self, _sleep):
        result = sample.lookup('词', max_pages=1, getter=lambda _: {'total': 31, 'items': [{'id': 1, 'term': '别词'}]})
        self.assertEqual(result['status'], 'incomplete')
        self.assertFalse(result['search_complete'])

    @patch('toocix_sample.time.sleep')
    @patch('toocix_sample.urlopen')
    def test_transient_failure_retried(self, open_url, _sleep):
        open_url.side_effect = [URLError('timeout'), URLError('timeout'), URLError('timeout')]
        with self.assertRaises(URLError):
            sample.fetch('https://toocix.com/', attempts=3)
        self.assertEqual(open_url.call_count, 3)

    @patch('toocix_sample.time.sleep')
    @patch('toocix_sample.urlopen')
    def test_rate_limit_not_retried(self, open_url, _sleep):
        open_url.side_effect = HTTPError('https://toocix.com/', 429, 'rate limit', {}, None)
        with self.assertRaises(HTTPError):
            sample.fetch('https://toocix.com/', attempts=3)
        self.assertEqual(open_url.call_count, 1)


if __name__ == '__main__':
    unittest.main()
