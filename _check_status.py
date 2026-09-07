# -*- coding: utf-8 -*-
import os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
for vol in ['econ-part2-lineage', 'psych-lineage', 'math-lineage',
            'truth-dimensions', 'marxism-lineage', 'economics-lineage', 'logic-lineage']:
    fp = os.path.join(ws, vol, vol + '.html')
    if os.path.exists(fp):
        c = open(fp, encoding='utf-8').read()
        has_phd = 'id="phd-prologue"' in c
        has_masters = 'id="masters-m1"' in c
        size = os.path.getsize(fp) // 1024
        print(f'{vol}: {size}KB, 博士模块={has_phd}, 硕士模块={has_masters}')
    else:
        print(f'{vol}: 文件不存在')