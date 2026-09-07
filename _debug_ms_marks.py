# -*- coding: utf-8 -*-
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    idx = c.find('硕士水平')
    if idx != -1:
        seg = c[max(0, idx-400):idx+300]
        classes = set(re.findall(r'class="([^"]+)"', seg))
        print(f'{vol}: 硕士模块附近 classes={sorted(classes)}')
        # 硕士模块的开头结构
        start = seg[:150].replace('\n', ' ⏎ ')
        print(f'   开头: {start}')
