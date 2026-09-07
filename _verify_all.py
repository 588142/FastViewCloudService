# -*- coding: utf-8 -*-
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = [
    'truth-dimensions', 'marxism-lineage', 'economics-lineage',
    'econ-part2-lineage', 'psych-lineage', 'math-lineage'
]
tags = ['div','section','figure','table','ul','ol','li','tr','td','th',
        'h2','h3','span','p','a','thead','tbody','nav','main','html']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    lines = c.count('\n') + 1
    zh = len(re.findall(r'[\u4e00-\u9fff]', c))
    appx = len(re.findall(r'id="appendix-[a-k]"', c))
    threejs = 1 if 'three.min.js' in c else 0
    chartjs = 1 if 'chart.js' in c else 0
    ends_ok = c.rstrip().endswith('</html>')
    
    bad = []
    for t in tags:
        o = len(re.findall(r'<%s(?=[\s>])' % t, c))
        cl = len(re.findall(r'</%s>' % t, c))
        if o != cl:
            bad.append(f'{t}({o}/{cl})')
            print(f'  {vol}: {t} 开={o} 闭={cl} MISMATCH')
    
    status = 'OK' if not bad else 'MISMATCH'
    print(f'{vol:25s} | 行={lines:5d} | 汉字={zh:6d} | 附录={appx:2d}/11 | Three.js={threejs} Chart.js={chartjs} | 结尾={ends_ok} | 标签={status}')

print('\n全部校验完成')