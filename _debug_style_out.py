# -*- coding: utf-8 -*-
"""定位head外的style块"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['economics-lineage', 'psych-lineage', 'math-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    hm = re.search(r'<head(?:\s[^>]*)?>', c)
    head_end = c.find('</head>', hm.end())
    print(f'\n=== {vol} ===')
    for m in re.finditer(r'<style', c):
        pos = m.start()
        line = c[:pos].count('\n') + 1
        loc = 'head内' if hm.end() <= pos < head_end else 'head外'
        # 找style块开头附近上下文
        ctx = c[max(0,pos-60):pos+80].replace('\n', ' ⏎ ')
        print(f'  @line {line} [{loc}]: {ctx[:150]}')
