# -*- coding: utf-8 -*-
import os, re
p = r'c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列\数学思想谱系\数学思想谱系.html'
c = open(p, encoding='utf-8').read()
refs = set(re.findall(r"url\(['\"]?([^'\"()]*_shared[^'\"()]*)['\"]?\)", c))
print('=== 数学思想谱系 字体引用 ===')
for r in sorted(refs):
    print(' ', r)
print()
q = r'c:\Users\Admin1\Documents\FastViewCloudService\math-lineage\math-lineage.html'
c2 = open(q, encoding='utf-8').read()
refs2 = set(re.findall(r"url\(['\"]?([^'\"()]*_shared[^'\"()]*)['\"]?\)", c2))
print('=== math-lineage 字体引用 ===')
for r in sorted(refs2):
    print(' ', r)
