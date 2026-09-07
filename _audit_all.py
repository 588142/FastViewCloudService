# -*- coding: utf-8 -*-
"""全面检查6卷：图片、链接、风格、布局"""
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    issues = []
    
    print(f'\n{"="*60}')
    print(f'检查: {vol}')
    
    # 1. 图片检查
    imgs = re.findall(r'<img[^>]+src="([^"]*)"', c)
    for src in imgs:
        if src.startswith('http://') or src.startswith('https://'):
            print(f'  [图片-外部] {src[:60]}')
        elif src.startswith('data:'):
            pass  # base64 正常
        elif src.startswith('_shared') or src.startswith('assets'):
            img_path = os.path.join(ws, vol, src)
            if not os.path.exists(img_path):
                issues.append(f'图片缺失: {src}')
        else:
            img_path = os.path.join(ws, vol, src)
            if not os.path.exists(img_path):
                issues.append(f'图片缺失: {src}')
    
    if not imgs:
        print('  [图片] 无<img>标签（使用CDN/Canvas可视化）')
    
    # 2. 外部资源检查
    external_js = re.findall(r'<script[^>]*src="([^"]*)"', c)
    for js in external_js:
        if js and not js.startswith('http') and not js.startswith('//'):
            js_path = os.path.join(ws, vol, js)
            if not os.path.exists(js_path):
                issues.append(f'脚本缺失: {js}')
    
    # 3. 内部锚点检查
    anchors = set(re.findall(r'id="([^"]*)"', c))
    links = re.findall(r'href="#([^"]*)"', c)
    for link in links:
        if link not in anchors:
            issues.append(f'断链: #{link} 无对应id')
    
    # 4. 跨卷链接检查
    cross_links = re.findall(r'href="(\.\./[^"]*)"', c)
    for cl in cross_links:
        cl_path = os.path.normpath(os.path.join(ws, vol, cl))
        if not os.path.exists(cl_path):
            issues.append(f'跨卷断链: {cl}')
    
    # 5. CSS变量一致性检查
    css_vars = set(re.findall(r'var\(--[^)]+\)', c))
    expected_vars = {'--bg','--bg2','--ink','--muted','--accent','--accent2','--rule','--font-head','--font-body'}
    missing_vars = expected_vars - css_vars
    if missing_vars:
        print(f'  [CSS] 缺少的变量: {missing_vars}')
    
    # 6. 布局比例检查
    fixed_widths = re.findall(r'width:\s*(\d+)(?:px|%)', c)
    big_fixed = [w for w in fixed_widths if int(w.replace('px','').replace('%','')) > 800 and 'px' in w]
    if big_fixed:
        for w in big_fixed:
            ctx = c[c.find(w)-30:c.find(w)+30]
            if 'max-width' not in ctx and 'max_width' not in ctx:
                issues.append(f'固定宽度可能溢出: {w} 附近: ...{ctx}...')
    
    # 7. Three.js 容器高度检查
    three_containers = re.findall(r'height:\s*(\d+)(?:px)', c)
    for h in three_containers:
        if int(h) < 300:
            issues.append(f'Three.js 容器高度可能太低: {h}px')
    
    # 8. 移动端适配检查
    if 'meta name="viewport"' not in c and 'viewport' not in c:
        print('  [响应式] 缺少 viewport meta 标签')
    
    # 输出结果
    if issues:
        print(f'  ⚠️ 发现 {len(issues)} 个问题:')
        for iss in issues[:10]:
            print(f'    - {iss}')
        if len(issues) > 10:
            print(f'    ... 还有 {len(issues)-10} 个')
    else:
        print(f'  ✅ 无问题')

print(f'\n{"="*60}')
print('检查完成')