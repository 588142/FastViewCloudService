# -*- coding: utf-8 -*-
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage']
tags = ['div','section','figure','table','ul','ol','li','tr','td','th',
        'h2','h3','span','p','a','nav','main','html']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    lines = c.count('\n') + 1
    zh = len(re.findall(r'[\u4e00-\u9fff]', c))
    appx = len(re.findall(r'id="appendix-[a-k]"', c))
    masters = len(re.findall(r'id="masters-m[1-8]"', c))
    phd_d = len(re.findall(r'id="phd-d[1-7]"', c))
    has_3d = 'three.min.js' in c
    has_chart = 'chart.js' in c
    ends_ok = c.rstrip().endswith('</html>')
    size = os.path.getsize(fp) // 1024
    
    bad = []
    for t in tags:
        o = len(re.findall(r'<%s(?=[\s>])' % t, c))
        cl = len(re.findall(r'</%s>' % t, c))
        if o != cl:
            bad.append(f'{t}({o}/{cl})')
    
    status = 'OK' if not bad else ','.join(bad[:2])
    print(f'{vol:25s} | {size:>3}KB | {lines:>4}行 | {zh:>5}字 | 本科{appx}/11 硕士{masters}/8 博士{phd_d}/7 | 3D={int(has_3d)} Chart={int(has_chart)} | {status}')