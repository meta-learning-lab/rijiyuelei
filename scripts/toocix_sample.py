#!/usr/bin/env python3
"""Query Toocix in small, resumable batches; store output privately as JSONL."""
import argparse
import json
import random
import socket
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = 'https://toocix.com/api/modern-dict/entries'
PAGE_SIZE = 30


def fetch(url, *, timeout=8, attempts=3, interval=1):
    for attempt in range(attempts):
        try:
            request = Request(url, headers={'User-Agent': 'rijiyuelei-research/1.0'})
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            # Do not retry rate limits or access restrictions automatically.
            if exc.code in (401, 403, 429) or not 500 <= exc.code < 600:
                raise
            error = exc
        except (URLError, TimeoutError, socket.timeout) as exc:
            error = exc
        if attempt + 1 == attempts:
            raise error
        time.sleep(interval * (2 ** attempt) + random.uniform(0, 0.2))


def lookup(word, *, max_pages=3, interval=1, getter=fetch):
    matches, total, pages = {}, None, 0
    for page in range(max_pages):
        query = urlencode({'q': word, 'limit': PAGE_SIZE, 'offset': page * PAGE_SIZE})
        found = getter(f'{BASE}?{query}')
        total = found['total']
        items = found['items']
        if not isinstance(items, list) or not isinstance(total, int):
            raise ValueError('Unexpected search response')
        pages += 1
        for item in items:
            if item.get('term') == word:
                matches[item['id']] = item
        if not items or pages * PAGE_SIZE >= total:
            break
        time.sleep(interval)
    entries = []
    for item_id in matches:
        time.sleep(interval)
        detail = getter(f'{BASE}/{item_id}')
        if detail.get('id') != item_id or detail.get('term') != word:
            raise ValueError('Detail response does not match search result')
        entries.append(detail)
    complete = pages * PAGE_SIZE >= total
    status = 'ok' if entries else ('not_found' if complete else 'incomplete')
    return {'word': word, 'status': status,
            'search_complete': complete, 'search_total': total, 'pages_checked': pages,
            'entries': entries, 'checked_at': datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('words', nargs='+')
    parser.add_argument('--output', required=True, help='Private JSONL file, appended and flushed per word')
    parser.add_argument('--max-pages', type=int, default=3)
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
