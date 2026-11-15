import csv,re,glob,collections,os,sys
from pathlib import Path
os.chdir(Path(__file__).resolve().parent.parent)
def read_rows(path):
 with open(path, encoding="utf-8-sig", newline="") as source:
  rows = {}
  for row in csv.DictReader(source):
   rid = row["ID"]
   if not rid or rid in rows:
    raise ValueError(f"{path}: ID 缺失或重复: {rid!r}")
   rows[rid] = row
  return rows

words=read_rows("dist/words.csv");poems=read_rows("dist/poems.csv");counts=collections.Counter();row_states=collections.defaultdict(collections.Counter);field_states=collections.defaultdict(collections.Counter);seen=set();errors=[]

def matches_pinyin(actual, candidate, status):
 if status == "缺失或无法确定":
  return actual == "?"
 if actual == "?":
  return status == "未核对"
 return actual == candidate

for fn in glob.glob('docs/逐项核对/*.md'):
 s=Path(fn).read_text(); isword=('写字表' in fn or '词语' in fn); ischar='写字表' in fn
 for section in re.split(r'(?m)^## ',s)[1:] if not (ischar and '一年级' in fn or ischar and '二年级上册' in fn) else [s]:
  header=section.splitlines()[0] if section else ''; m=re.search(r'（([pw][\w-]+)）',header);rid=m[1] if m else ''
  for line in section.splitlines():
   a=[x.strip() for x in line.strip('|').split('|')];key=None;status=a[-1]
   try:
    if ischar and len(a)==9 and a[0] in words and a[3].isdigit():
     r=words[a[0]];j=int(a[3])-1;assert r['汉字'][j]==a[4] and matches_pinyin(r['汉字拼音'].split()[j],a[5],status);key=('w',a[0],'c',j);status=a[-1]
    elif ischar and len(a)==8 and a[0] in words and a[2].isdigit():
     r=words[a[0]];j=int(a[2])-1;assert r['汉字'][j]==a[3] and matches_pinyin(r['汉字拼音'].split()[j],a[4],status) and a[4]==a[6];key=('w',a[0],'c',j);status=a[-1]
    elif ischar and len(a)==6 and rid in words and a[0].isdigit():
     r=words[rid];j=int(a[0])-1;assert r['汉字'][j]==a[1] and matches_pinyin(r['汉字拼音'].split()[j],a[2],status);key=('w',rid,'c',j);status=a[-1]
    elif isword and not ischar and len(a) in (8,9) and rid in words and a[0].isdigit() and a[2].isdigit():
     r=words[rid];i,j=int(a[0])-1,int(a[2])-1;assert r['词语'].split('|')[i]==a[1] and a[1][j]==a[3] and matches_pinyin(r['词语拼音'].split('|')[i].split()[j],a[4],status);key=('w',rid,'t',i,j);status=a[-1]
    elif not isword and len(a)>=6 and rid in poems and a[0].isdigit() and a[1].isdigit():
     r=poems[rid];i,j=int(a[0])-1,int(a[1])-1;chars=re.findall('[\u3400-\u9fff]',r['正文'].split('\\n')[i]);ps=r['正文拼音'].split('\\n')[i].split();assert chars[j]==a[2] and matches_pinyin(ps[j].strip('，。！？；：、,.!;:'),a[3],status);key=('p',rid,i,j);status=a[-1]
    if key:
     assert key not in seen,(key,'重复');seen.add(key);assert status in ('已核对','已核对，有分歧','未核对','缺失或无法确定'),(key,status);counts[(key[0],status)]+=1;row_states[(key[0],key[1])][status]+=1;field_states[(key[0],key[1],"正文" if key[0]=="p" else ("汉字" if key[2]=="c" else "词语"))][status]+=1
   except (AssertionError,IndexError,ValueError) as e:errors.append((fn,rid,line[:100],str(e)))
for category, rows in (("w", words), ("p", poems)):
 for rid, row in rows.items():
  if row["核对状态"].startswith("已核对"):
   states = row_states[(category, rid)]
   if states["未核对"] or states["缺失或无法确定"]:
    errors.append((category, rid, "CSV 标记已核对，但逐项记录仍有未确认音节", dict(states)))
expected = sum(len(re.findall(r"[\u3400-\u9fff]", row["汉字"] + row["词语"])) for row in words.values())
expected += sum(len(re.findall(r"[\u3400-\u9fff]", row["正文"])) for row in poems.values())
if errors or len(seen) > expected:
 print("统计失败：逐项记录有错误", errors[:10], file=sys.stderr)
 sys.exit(1)
complete = sum(n for (_, state), n in counts.items() if state in ("已核对", "已核对，有分歧"))
print(f"已核对：{complete} / {expected}（{complete / expected * 100:.2f}%）" if expected else "已核对：0 / 0（无数据）")
for state in ("已核对", "已核对，有分歧", "缺失或无法确定", "未核对"):
 print(f"{state}：{sum(n for (_, label), n in counts.items() if label == state)}")
print(f"未建立逐项记录：{expected - len(seen)}")
print("单位：CSV 中每次汉字出现；此比例不代表教材范围完整或拼音准确率。")
for grade in ("一年级", "二年级", "三年级", "四年级", "五年级", "六年级"):
 for term in ("上册", "下册"):
  subset = [(category, row) for category, rows in (("w", words), ("p", poems)) for row in rows.values() if row["年级"] == grade and row["学期"] == term]
  total = sum(len(re.findall(r"[\u3400-\u9fff]", row["汉字"] + row["词语"] if category == "w" else row["正文"])) for category, row in subset)
  states = collections.Counter()
  for category, row in subset:
   states.update(row_states[(category, row["ID"])])
  verified = states["已核对"] + states["已核对，有分歧"]
  missing_records = total - sum(states.values())
  print(f"{grade}{term}：{verified}/{total}，有分歧 {states['已核对，有分歧']}，无法确定 {states['缺失或无法确定']}，未核对 {states['未核对']}，无记录 {missing_records}")
  for category, field in (("w", "汉字"), ("w", "词语"), ("p", "正文")):
   matching = [row for c, row in subset if c == category]
   field_total = sum(len(re.findall(r"[\u3400-\u9fff]", row[field])) for row in matching)
   field_count = collections.Counter()
   for row in matching:
    field_count.update(field_states[(category, row["ID"], field)])
   field_complete = field_count["已核对"] + field_count["已核对，有分歧"]
   print(f"  {field}：{field_complete}/{field_total}，有分歧 {field_count['已核对，有分歧']}，无法确定 {field_count['缺失或无法确定']}，未核对 {field_count['未核对']}，无记录 {field_total - sum(field_count.values())}")
