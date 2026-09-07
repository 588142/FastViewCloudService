# -*- coding: utf-8 -*-
"""检查getCenterPoint/afterDraw模式在所有卷中的分布"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    n_gc = len(re.findall(r'getCenterPoint\(\)', c))
    n_ad = len(re.findall(r'afterDraw', c))
    n_map = len(re.findall(r'datasets:\s*methods\.map', c))
    n_ctxlabel = len(re.findall(r'context\.dataset\.label', c))
    print(f'{vol}: getCenterPoint={n_gc} afterDraw={n_ad} datasets.map={n_map} dataset.label={n_ctxlabel}')
