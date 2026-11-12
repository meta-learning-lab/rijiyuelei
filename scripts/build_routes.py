"""Generate a static entry page for each CSV record."""
import csv
import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
out = root / 'dist'
html = (out / 'index.html').read_text(encoding='utf-8')
routes = []


def check_pinyin(text, pinyin, context):
    if not pinyin.strip():
        return
    syllables = pinyin.replace('\\n', ' ').split()
    count = len(re.findall(r'[\u3400-\u9fff]', text))
    if len(syllables) != count:
        raise ValueError(f'{context}: {count} 个汉字与 {len(syllables)} 个拼音不对应')

for category, filename, title in [('words', 'words.csv', '课文'), ('poems', 'poems.csv', '标题')]:
    seen = set()
    with (out / filename).open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            item_id = row.get('ID', '')
            parts = [item_id, row.get('年级', ''), row.get('学期', ''), row.get(title, '')]
            if not re.fullmatch(r'[A-Za-z0-9_-]+', item_id) or item_id in seen:
                raise ValueError(f'{filename}: ID 缺失、重复或格式不正确: {item_id!r}')
            if any(not part or part in ('.', '..') or '/' in part or '\\' in part for part in parts):
                raise ValueError(f'{filename}: URL 字段不能为空或包含路径分隔符: {parts!r}')
            if category == 'words' and not (row.get('汉字', '').strip() or row.get('词语', '').strip()):
                raise ValueError(f'{filename}: {item_id} 的汉字和词语不能同时为空')
            if row['年级'] not in ['一年级','二年级','三年级','四年级','五年级','六年级'] or row['学期'] not in ['上册','下册']:
                raise ValueError(f'{filename}: {item_id} 的年级或学期不正确')
            if category == 'words':
                check_pinyin(row.get('汉字', ''), row.get('汉字拼音', ''), f'{item_id} 汉字')
                terms = row.get('词语', '').split('|') if row.get('词语', '') else []
                pronunciation = row.get('词语拼音', '')
                if pronunciation.strip():
                    groups = pronunciation.split('|')
                    if len(groups) != len(terms):
                        raise ValueError(f'{item_id}: 词语和拼音分组数量不一致')
                    for term, py in zip(terms, groups):
                        check_pinyin(term, py, f'{item_id} 词语 {term}')
            else:
                check_pinyin(row.get('正文', ''), row.get('正文拼音', ''), f'{item_id} 正文')
            seen.add(item_id)
            routes.append((category, parts))
for category in ('words', 'poems'):
    target = out / category
    if target.exists():
        shutil.rmtree(target)
for category, parts in routes:
    folder = out.joinpath(category, *parts)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(html, encoding='utf-8')
print(f'已生成 {len(routes)} 个内容页面')
