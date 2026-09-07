# -*- coding: utf-8 -*-
"""修复所有检查发现的问题：CDN重复加载、容器高度、CSS变量、断链"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage']

# 1. 检查 --font-body 是否真的被使用
print('=== 1. --font-body 使用情况 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    if 'var(--font-body)' in c:
        print(f'{vol}: 使用了 --font-body')
    else:
        print(f'{vol}: 未使用 --font-body (定义缺失但无影响)')

# 2. 修复 CDN 重复加载：移除所有重复的 three.min.js 和 chart.js 加载
# 策略：保留第一个，移除后续的重复加载
print('\n=== 2. 修复CDN重复加载 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    
    # 统计原本数量
    orig_three = len(re.findall(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c))
    orig_chart = len(re.findall(r'<script[^>]*src="[^"]*chart\.js[^"]*"', c))
    
    # 找到第一个 three.min.js 加载，保留它，移除后续的
    three_scripts = list(re.finditer(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c))
    if len(three_scripts) > 1:
        # 从后往前删，保留第一个
        for m in reversed(three_scripts[1:]):
            c = c[:m.start()] + '<!-- three.min.js 已在上方加载 -->' + c[m.end():]
    
    # 同样处理 chart.js
    chart_scripts = list(re.finditer(r'<script[^>]*src="[^"]*chart\.js[^"]*"', c))
    if len(chart_scripts) > 1:
        for m in reversed(chart_scripts[1:]):
            c = c[:m.start()] + '<!-- chart.js 已在上方加载 -->' + c[m.end():]
    
    # 写回
    open(fp, 'w', encoding='utf-8').write(c)
    
    # 验证
    new_three = len(re.findall(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c))
    new_chart = len(re.findall(r'<script[^>]*src="[^"]*chart\.js[^"]*"', c))
    print(f'{vol}: Three.js {orig_three}→{new_three} Chart.js {orig_chart}→{new_chart}')

# 3. 修复 280px 容器高度
print('\n=== 3. 修复容器高度 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    old = c
    # 替换 height:280px 为 height:360px
    c = c.replace('height:280px', 'height:360px')
    c = c.replace('height:280px', 'height:360px')  # 再查一次
    if c != old:
        open(fp, 'w', encoding='utf-8').write(c)
        print(f'{vol}: 高度已修复 280px→360px')
    else:
        print(f'{vol}: 无280px高度')

# 4. 检查跨卷断链
print('\n=== 4. 跨卷链接 ===')
ism_path = os.path.join(ws, 'isms-glossary', 'isms-lineage.html')
if not os.path.exists(ism_path):
    # 尝试其他可能的路径
    ism_alt = os.path.join(ws, 'isms-glossary', 'isms-glossary.html')
    if os.path.exists(ism_alt):
        print(f'isms-lineage.html 不存在，但有 isms-glossary.html')
        # 修复 truth-dimensions 中的链接
        fp = os.path.join(ws, 'truth-dimensions', 'truth-dimensions.html')
        c = open(fp, encoding='utf-8').read()
        if '../isms-glossary/isms-lineage.html' in c:
            c = c.replace('../isms-glossary/isms-lineage.html', '../isms-glossary/isms-glossary.html')
            open(fp, 'w', encoding='utf-8').write(c)
            print('truth-dimensions: 链接已修复 -> isms-glossary.html')
    else:
        print(f'isms-glossary 目录也不存在')
else:
    print('isms-lineage.html 存在')

# 5. 验证修复结果
print('\n=== 5. 最终验证 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    three_c = len(re.findall(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c))
    chart_c = len(re.findall(r'<script[^>]*src="[^"]*chart\.js[^"]*"', c))
    low_height = 'height:280px' in c
    font_body_used = 'var(--font-body)' in c
    print(f'{vol}: Three.js={three_c} Chart.js={chart_c} 低高度={low_height} font-body使用={font_body_used}')

print('\n修复完成')