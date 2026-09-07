# -*- coding: utf-8 -*-
"""扫描7个标星卷的所有跨卷链接目标目录"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

targets = set()
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    for m in re.finditer(r'href="\.\./([^/"]+)/', c):
        targets.add(m.group(1))

print(f'链接目标目录 ({len(targets)}):')
for t in sorted(targets):
    print(f'  {t}')
