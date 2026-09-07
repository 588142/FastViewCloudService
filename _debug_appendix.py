# -*- coding: utf-8 -*-
"""查看附录section的结构和样式"""
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    # 找appendix-a section
    idx = c.find('id="appendix-a"')
    if idx == -1:
        print(f'{vol}: 无appendix-a')
        continue
    # 往前找section开标签
    sec_start = c.rfind('<section', 0, idx)
    seg = c[sec_start:idx+120]
    seg1 = seg.replace('\n', ' ⏎ ')
    print(f'{vol}: appendix-a结构: {seg1[:220]}')
