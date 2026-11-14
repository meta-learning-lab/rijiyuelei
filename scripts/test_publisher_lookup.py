import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import publisher_lookup as publisher


class PublisherTests(unittest.TestCase):
    @patch('publisher_lookup.time.sleep')
    def test_exact_matches_multiple_readings_and_books(self, _sleep):
        def get(url):
            if 'pageNo=1' in url:
                return {'code': 200, 'totalPage': 2, 'books': [
                    {'bookId': 1, 'items': [{'uuid': 'bad', 'name': '行', 'phoneticTranscription': 'wrong'}]},
                    {'bookId': 2, 'items': [{'uuid': '1', 'name': '<span>行</span>', 'phoneticTranscription': 'háng'},
                                             {'uuid': 'bad2', 'name': '行走', 'phoneticTranscription': 'wrong'}]}]}
            return {'code': 200, 'totalPage': 2, 'books': [{'bookId': 2, 'items': [
                {'uuid': '1', 'name': '行', 'phoneticTranscription': 'háng'},
                {'uuid': '2', 'name': '行', 'phoneticTranscription': 'xíng'}]}]}
        result = publisher.lookup('行', getter=get)
        self.assertTrue(result['search_complete'])
        self.assertEqual([e['pinyin'] for e in result['entries']], ['háng', 'xíng'])

    def test_truncated_search_and_missing_results(self):
        get = lambda _: {'code': 200, 'totalPage': 2, 'books': []}
        result = publisher.lookup('词', max_pages=1, getter=get)
        self.assertEqual(result['status'], 'incomplete')
        self.assertFalse(result['search_complete'])

    def test_business_error_is_not_missing(self):
        with self.assertRaises(ValueError):
            publisher.lookup('词', getter=lambda _: {'code': 500, 'books': []})

    def test_missing_pronunciation_is_error(self):
        response = {'code': 200, 'totalPage': 1, 'books': [
            {'bookId': 2, 'items': [{'uuid': '1', 'name': '词'}]}]}
        with self.assertRaises(ValueError):
            publisher.lookup('词', getter=lambda _: response)

    @patch('publisher_lookup.time.sleep')
    @patch('publisher_lookup.urlopen')
    def test_transient_errors_are_retried(self, open_url, _sleep):
        open_url.side_effect = URLError('timeout')
        with self.assertRaises(URLError):
            publisher.fetch('https://bjzs.vdict.com.cn/', attempts=3)
        self.assertEqual(open_url.call_count, 3)

    @patch('publisher_lookup.time.sleep')
    @patch('publisher_lookup.urlopen')
    def test_rate_limit_is_not_retried(self, open_url, _sleep):
        open_url.side_effect = HTTPError('https://bjzs.vdict.com.cn/', 429, 'rate limit', {}, None)
        with self.assertRaises(HTTPError):
            publisher.fetch('https://bjzs.vdict.com.cn/', attempts=3)
        self.assertEqual(open_url.call_count, 1)


if __name__ == '__main__':
    unittest.main()
