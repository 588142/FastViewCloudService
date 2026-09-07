# -*- coding: utf-8 -*-
"""检查 marxism 内容重复 + 主题索引实际文件验证"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
desktop = r'c:\Users\Admin1\Desktop\Trae资料库'

# 1. 检查 marxism 中关键句子的重复次数
print('=== marxism 重复内容检查 ===')
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

key_phrases = [
    '毛泽东面对的是',
    '苏联解体也可以用唯物史观分析',
    '空想社会主义（对资本主义的批判',
    '站在巨人肩膀上',
]
for phrase in key_phrases:
    count = c.count(phrase)
    print(f'  "{phrase[:20]}...": {count} 次')

# 检查 id 重复
print('\n=== id 重复检查 ===')
ids = re.findall(r'id="([^"]*)"', c)
dup_ids = {i for i in ids if ids.count(i) > 1}
print(f'总id数: {len(ids)}, 重复id: {len(dup_ids)}')
for d in sorted(dup_ids)[:10]:
    print(f'  {d}')

# 检查博士/硕士模块重复
print('\n=== 模块重复检查 ===')
for m in re.finditer(r'id="(masters-m\d|phd-[a-z]+|appendix-[a-z]+)"', c):
    print(f'  {m.group(1)} @ {m.start()}')

# 2. 桌面版 东方思想谱系 目录实际文件
print('\n=== 桌面版东方思想谱系文件 ===')
dp = os.path.join(desktop, '东方思想谱系')
if os.path.exists(dp):
    print(f'  {[f for f in os.listdir(dp) if f.endswith(".html")]}')

# 3. 主题索引中的 eastern-thought.html 链接验证
print('\n=== 桌面版主题索引 eastern-thought 链接 ===')
dt_fp = os.path.join(desktop, '思想图谱系列', '主题索引.html')
dc = open(dt_fp, encoding='utf-8').read()
for m in re.finditer(r'href="\.\./([^"]*eastern[^"]*)"', dc):
    target = os.path.normpath(os.path.join(desktop, '思想图谱系列', '..', m.group(1)))
    print(f'  {m.group(1)} -> 存在={os.path.exists(target)}')

# 4. 工作区主题索引 vs 桌面版 内容结构对比
print('\n=== 主题索引内容对比 ===')
ws_fp = os.path.join(ws, '思想图谱系列', '主题索引.html')
wc = open(ws_fp, encoding='utf-8').read()

# 提取每条索引条目（比较主要文本内容，忽略链接路径）
def extract_items(c):
    # 提取 li 或 p 中的文本内容
    items = re.findall(r'<li[^>]*>(.*?)</li>', c, re.DOTALL)
    texts = set()
    for it in items:
        # 去标签
        txt = re.sub(r'<[^>]+>', '', it)
        txt = txt.strip()
        if txt:
            texts.add(txt)
    return texts

ws_items = extract_items(wc)
dt_items = extract_items(dc)
print(f'工作区条目: {len(ws_items)}, 桌面条目: {len(dt_items)}')
print(f'仅工作区: {len(ws_items - dt_items)}')
print(f'仅桌面: {len(dt_items - ws_items)}')
for t in sorted(ws_items - dt_items)[:5]:
    print(f'  WS: {t[:60]}')
for t in sorted(dt_items - ws_items)[:5]:
    print(f'  DT: {t[:60]}')