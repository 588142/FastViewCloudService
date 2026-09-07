# -*- coding: utf-8 -*-
"""分析每个标星卷的文档框架结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    
    print(f'\n{"="*70}')
    print(f'卷: {vol} ({len(c)} 字符)')
    
    # 列出所有 DOCTYPE / html / head / body / /body / /html 位置
    marks = []
    for t in ['<!DOCTYPE', '<head', '</head>', '<body', '</body>', '</html>']:
        for m in re.finditer(re.escape(t), c, re.IGNORECASE):
            marks.append((m.start(), t))
    marks.sort()
    
    for pos, t in marks:
        print(f'  {pos:>7}  {t}')
    
    # 统计各模块的section数量（按body分段）
    print('  --- section 统计 ---')
    body_starts = [pos for pos, t in marks if t == '<body']
    body_starts.append(len(c))
    for i in range(len(body_starts)-1):
        seg = c[body_starts[i]:body_starts[i+1]]
        opens = len(re.findall(r'<section\b', seg))
        closes = len(re.findall(r'</section>', seg))
        # 找该段的标题
        titles = re.findall(r'<title>(.*?)</title>', seg)
        print(f'  body[{i}] @ {body_starts[i]}: section {opens}开/{closes}闭, title={titles[:1]}')