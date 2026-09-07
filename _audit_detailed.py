# -*- coding: utf-8 -*-
"""详细检查CSS变量、跨卷链接、3D容器等"""
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage']

print('=== 1. CSS变量定义检查 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    vars_defined = set(re.findall(r'--([\w-]+)\s*:', c))
    expected = {'bg','bg2','ink','muted','accent','accent2','rule','font-head','font-body'}
    present = {'--'+v for v in expected if v in vars_defined}
    missing = {'--'+v for v in expected if v not in vars_defined}
    if missing:
        print(f'{vol}: 缺少定义: {missing}')
    else:
        print(f'{vol}: 全部已定义 ✅')

print('\n=== 2. 跨卷链接检查 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    cross = re.findall(r'href="(\.\./(?:[^"]*))"', c)
    bad = []
    for cl in cross:
        cl_path = os.path.join(ws, vol, cl)
        if not os.path.exists(cl_path):
            bad.append(cl)
    if bad:
        print(f'{vol}: 断链: {bad}')
    else:
        print(f'{vol}: 全部正常 ✅ ({len(cross)}个跨卷链接)')

print('\n=== 3. Three.js/CDN引用检查 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    three_refs = re.findall(r'<script[^>]*src="[^"]*three[^"]*"', c)
    chart_refs = re.findall(r'<script[^>]*src="[^"]*chart\.js[^"]*"', c)
    # 检查是否有重复加载
    three_count = len(three_refs)
    chart_count = len(chart_refs)
    dup_issues = []
    if three_count > 1:
        dup_issues.append(f'Three.js重复加载{three_count}次')
    if chart_count > 1:
        dup_issues.append(f'Chart.js重复加载{chart_count}次')
    if dup_issues:
        print(f'{vol}: ⚠️ {", ".join(dup_issues)}')
    else:
        print(f'{vol}: CDN引用正常 ✅')

print('\n=== 4. 3D容器高度检查 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    # 找所有 Three.js 可视化容器的 style 中的 height
    heights = re.findall(r'viz-container[^>]*style="[^"]*height:(\d+)px', c)
    viz_heights = re.findall(r'(?:canvas|div)[^>]*style="[^"]*height:(\d+)px', c)
    for h in set(heights + viz_heights):
        if int(h) < 300:
            print(f'{vol}: 有容器高度={h}px (建议≥300px)')

print('\n=== 5. 响应式布局检查 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    if 'viewport' not in c:
        print(f'{vol}: 缺少viewport meta标签')
    if '@media' not in c:
        print(f'{vol}: 缺少媒体查询')

print('\n检查完成')