#!/usr/bin/env python3
"""Query publisher search results in small, resumable batches.

The endpoint is used by the publisher's website, not a documented public API.
Results are pronunciation candidates and still require textbook/context review.
"""
import argparse
from html.parser import HTMLParser
import json
import random
import socket
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = 'https://bjzs.vdict.com.cn/api/front/search/turnPage'


def fetch(url, *, timeout=8, attempts=3, interval=1):
    for attempt in range(attempts):
        try:
            request = Request(url, headers={'User-Agent': 'rijiyuelei-research/1.0'})
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code in (401, 403, 429) or not 500 <= exc.code < 600:
                raise
            error = exc
        except (URLError, TimeoutError, socket.timeout) as exc:
            error = exc
        if attempt + 1 == attempts:
            raise error
        time.sleep(interval * (2 ** attempt) + random.uniform(0, 0.2))


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)


def text(value):
    parser = Text()
    parser.feed(value or '')
    return ''.join(parser.parts).strip()


def lookup(word, *, max_pages=5, interval=1, getter=fetch):
    matches, total_pages, pages_checked = {}, None, 0
    for page in range(1, max_pages + 1):
        url = f'{BASE}?{urlencode({"input": word, "pageNo": page})}'
        data = getter(url)
        if data.get('code') != 200 or not isinstance(data.get('books'), list):
            raise ValueError('Publisher returned an invalid or unsuccessful response')
        total_pages = data.get('totalPage')
        if not isinstance(total_pages, int) or total_pages < 0:
            raise ValueError('Publisher did not provide a valid page count')
        pages_checked += 1
        for book in data['books']:
            if book.get('bookId') != 2:
                continue
            for entry in book.get('items', []):
                if text(entry.get('name')) != word:
                    continue
                entry_id = entry.get('uuid')
                pronunciation = entry.get('phoneticTranscription')
                if not entry_id or not pronunciation:
                    raise ValueError('Exact match lacks ID or pronunciation')
                matches[entry_id] = {
                    'id': entry_id, 'pinyin': pronunciation,
                    'summary': text(entry.get('summaryMobile')),
                    'detail_url': 'https://bjzs.vdict.com.cn/SY/detail/' + entry_id,
                }
        if page >= total_pages:
            break
        time.sleep(interval)
    complete = pages_checked >= total_pages
    return {'word': word, 'status': 'ok' if matches else ('not_found' if complete else 'incomplete'),
            'search_complete': complete, 'pages_checked': pages_checked,
            'total_pages': total_pages, 'book_id': 2, 'entries': list(matches.values()),
            'checked_at': datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('words', nargs='+')
    parser.add_argument('--output', required=True, help='Private JSONL path; appended per word')
    parser.add_argument('--max-pages', type=int, default=5)
    parser.add_argument('--interval', type=float, default=1)
    args = parser.parse_args()
    if args.max_pages < 1 or args.interval < 1:
        parser.error('max-pages must be >= 1 and interval >= 1 second')
    done = set()
    try:
        with open(args.output, encoding='utf-8') as source:
            for line in source:
                record = json.loads(line)
                if record.get('status') == 'ok' and record.get('search_complete'):
                    done.add(record['word'])
    except FileNotFoundError:
        pass
    failed = False
    with open(args.output, 'a', encoding='utf-8') as out:
        for word in dict.fromkeys(args.words):
            if word in done:
                print(f'{word}: skipped (complete)', file=sys.stderr)
                continue
            stop = False
            try:
                record = lookup(word, max_pages=args.max_pages, interval=args.interval,
                                getter=lambda url: fetch(url, interval=args.interval))
            except HTTPError as exc:
                failed = True
                stop = exc.code in (401, 403, 429)
                record = {'word': word, 'status': 'error', 'error': str(exc),
                          'checked_at': datetime.now(timezone.utc).isoformat()}
            except (URLError, TimeoutError, socket.timeout, ValueError, KeyError, json.JSONDecodeError) as exc:
                failed = True
                record = {'word': word, 'status': 'error', 'error': str(exc),
                          'checked_at': datetime.now(timezone.utc).isoformat()}
            out.write(json.dumps(record, ensure_ascii=False) + '\n')
            out.flush()
            print(f"{word}: {record['status']}" + ('' if record.get('search_complete', True) else ' (search incomplete)'), file=sys.stderr)
            if stop:
                print('Access restriction or rate limit; stopping batch.', file=sys.stderr)
                break
            time.sleep(args.interval)
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
