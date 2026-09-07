# -*- coding: utf-8 -*-
"""终审：排除注释中的CDN引用"""
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage']

print('=== 最终审计 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    # 移除注释块
    c_no_comment = re.sub(r'<!--.*?-->', '', c, flags=re.DOTALL)
    
    three_c = len(re.findall(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c_no_comment))
    chart_c = len(re.findall(r'<script[^>]*src="[^"]*chart\.js[^"]*"', c_no_comment))
    low_h = 'height:280px' in c_no_comment
    ends_ok = c.rstrip().endswith('</html>')
    size = os.path.getsize(fp) // 1024
    
    anchors = set(re.findall(r'id="([^"]*)"', c))
    broken = []
    for link in re.findall(r'href="#([^"]*)"', c):
        if link not in anchors:
            broken.append(link)
    
    cross = re.findall(r'href="(\.\./(?:[^"]*))"', c)
    cross_bad = []
    for cl in cross:
        if not os.path.exists(os.path.join(ws, vol, cl)):
            cross_bad.append(cl)
    
    issues = []
    if three_c > 1: issues.append(f'Three.js x{three_c}')
    if chart_c > 1: issues.append(f'Chart.js x{chart_c}')
    if low_h: issues.append('低高度')
    if broken: issues.append(f'锚点断链:{broken[:3]}')
    if cross_bad: issues.append(f'跨卷断链:{cross_bad}')
    
    status = '✅' if not issues else '⚠️'
    detail = ', '.join(issues) if issues else 'OK'
    print(f'{vol:25s} | {size:>3}KB | 3D={three_c} Chart={chart_c} | {status} {detail}')

print('审计完成')