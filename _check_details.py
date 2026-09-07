# -*- coding: utf-8 -*-
"""检查各卷：关联辑目 section、内嵌head内容"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    
    print(f'\n{"="*60}')
    print(f'卷: {vol}')
    
    # 1. 关联辑目 section
    gj = c.count('关联辑目')
    print(f'  "关联辑目"出现次数: {gj}')
    for m in re.finditer('关联辑目', c):
        print(f'    @{m.start()}')
    
    # 2. 所有 <head> 的非style内容
    heads = [(m.start(), m.end()) for m in re.finditer(r'<head[^>]*>', c, re.IGNORECASE)]
    print(f'  <head> 数量: {len(heads)}')
    for i, (hs, he) in enumerate(heads):
        # 找对应 </head>
        hclose = c.find('</head>', he)
        if hclose == -1:
            hclose = he + 1000
        seg = c[he:hclose]
        # 统计非style内容
        no_style = re.sub(r'<style[^>]*>.*?</style>', '', seg, flags=re.DOTALL).strip()
        if no_style:
            print(f'    head[{i}] @{hs} 非style内容: {no_style[:150]}')
        else:
            print(f'    head[{i}] @{hs} 仅style')
    
    # 3. 各body段的section（含id）
    bodies = [m.start() for m in re.finditer(r'<body[^>]*>', c, re.IGNORECASE)]
    bodies.append(len(c))
    print(f'  <body> 数量: {len(bodies)-1}')
    for i in range(len(bodies)-1):
        seg = c[bodies[i]:bodies[i+1]]
        sec_ids = re.findall(r'<section[^>]*id="([^"]*)"', seg)
        print(f'    body[{i}] @{bodies[i]}: {len(sec_ids)}个section: {sec_ids[:5]}...')