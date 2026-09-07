# -*- coding: utf-8 -*-
"""查找Three.js LineBasicMaterial的dashed参数"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    for m in re.finditer(r'LineBasicMaterial', c):
        idx = m.start()
        line = c[:idx].count('\n') + 1
        seg = c[idx:idx+220].replace('\n', ' ')
        if 'dashed' in seg or 'dashSize' in seg or 'gapSize' in seg:
            print(f'{vol} @line {line}:')
            print(f'  {seg[:220]}')
            print()
