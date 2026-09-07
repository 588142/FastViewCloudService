# -*- coding: utf-8 -*-
"""确认politics-lineage和isms-glossary在桌面版的对应目录"""
import os, re, glob

dt = r'c:\Users\Admin1\Desktop\Trae资料库'
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

# 1. politics-lineage 的标题
fp = os.path.join(ws, 'politics-lineage', 'politics-lineage.html')
c = open(fp, encoding='utf-8').read()
t = re.search(r'<title>(.*?)</title>', c, re.DOTALL)
print(f'politics-lineage 标题: {t.group(1) if t else "?"}')

# 2. 桌面版 政治学通论 和 政治基础概念1 的文件
for d in ['政治学通论', '政治基础概念1']:
    files = glob.glob(os.path.join(dt, d, '*.html'))
    print(f'{d}: {[os.path.basename(f) for f in files[:5]]}')
    for f in files[:1]:
        c2 = open(f, encoding='utf-8').read()
        t2 = re.search(r'<title>(.*?)</title>', c2, re.DOTALL)
        print(f'  → 标题: {t2.group(1) if t2 else "?"}')

# 3. isms-glossary 是否存在对应
print(f'\nisms-glossary 桌面目录: {os.path.exists(os.path.join(dt, "isms-glossary"))}')
# 找含"主义"或"流派"的目录
for d in os.listdir(dt):
    if '主义' in d or '流派' in d or 'ism' in d.lower():
        print(f'  候选: {d}')
