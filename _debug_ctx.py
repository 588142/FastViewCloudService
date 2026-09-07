# -*- coding: utf-8 -*-
"""检查4个重复段落的上下文结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

positions = [m.start() for m in re.finditer('毛泽东面对的是', c)]
for idx, start in enumerate(positions):
    print(f'\n{"="*70}')
    print(f'段落{idx+1} @ 位置{start}')
    # 往前找块的开始（前一个 </div> 或 <section 或 <div class="callout">
    # 取前后各600字符
    ctx = c[max(0, start-600):start+600]
    print(f'上下文:')
    print(ctx)
    print()