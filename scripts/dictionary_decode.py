#!/usr/bin/env python3
"""Decode a locally saved sample from dictionary_sample.js; never stores credentials."""
import argparse
import json
import re
from html.parser import HTMLParser
from io import BytesIO
from urllib.request import urlopen

from fontTools.ttLib import TTFont


class TextExtractor(HTMLParser):
    def __init__(self, mapping):
        super().__init__(convert_charrefs=True)
        self.mapping = mapping
        self.parts = []
        self.unmapped = set()

    def handle_data(self, data):
        for char in data:
            if '\u4e00' <= char <= '\u9fff' and ord(char) not in self.mapping:
                self.unmapped.add(char)
            self.parts.append(self.mapping.get(ord(char), char))

    def handle_endtag(self, tag):
        if tag in {'li', 'p', 'div'}:
            self.parts.append('\n')


def mapping_for(fonts):
    folder, digest = fonts['folder'], fonts['md5']
    if not re.fullmatch(r'\d{8}', folder) or not re.fullmatch(r'[0-9a-f]{32}', digest):
        raise ValueError('Invalid font location')
    mapping = {}
    for font_id in fonts['pathArray']:
        if not re.fullmatch(r'\d+', font_id):
            raise ValueError('Invalid font identifier')
        url = f'https://bjzs.vdict.com.cn/font/{folder}/{digest}/{font_id}.woff'
        with urlopen(url, timeout=20) as response:
            font = TTFont(BytesIO(response.read()))
        for code, name in font.getBestCmap().items():
            match = re.fullmatch(r'uni([0-9A-Fa-f]{4,6})', name)
            if match:
                value = chr(int(match.group(1), 16))
                if code in mapping and mapping[code] != value:
                    raise ValueError('Conflicting glyph mapping')
                mapping[code] = value
    return mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Local JSON output of the browser sample')
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as f:
        entries = json.load(f)
    for entry in entries:
        if entry.get('error'):
            print(json.dumps(entry, ensure_ascii=False))
            continue
        try:
            extractor = TextExtractor(mapping_for(entry['fonts']))
            extractor.feed(entry['html'])
            print(json.dumps({'word': entry['word'], 'uuid': entry['uuid'], 'pinyin': entry['pinyin'], 'text': ''.join(extractor.parts).strip(), 'unmapped': sorted(extractor.unmapped)}, ensure_ascii=False))
        except Exception as error:
            print(json.dumps({'word': entry['word'], 'uuid': entry.get('uuid'), 'error': str(error)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
