# -*- coding: utf-8 -*-
"""验证style/script合并完整性 + 检查style是否都在head内"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

print(f'{"卷":26s} | {"style":>3s} | {"script":>3s} | CSS vars | @media | 关键样式')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()

    # head边界
    hm = re.search(r'<head(?:\s[^>]*)?>', c)
    head_end = c.find('</head>', hm.end())
    head_content = c[hm.end():head_end]

    n_style_total = len(re.findall(r'<style', c))
    n_style_head = len(re.findall(r'<style', head_content))
    n_script = len(re.findall(r'<script', c))

    # CSS完整性
    has_root = ':root' in c
    n_media = len(re.findall(r'@media', c))
    n_vars = len(re.findall(r'--[a-z-]+:', c))
    # 关键类
    classes = ['.sidenav', '.callout', '.table-wrap', '.viz-container', '.sec', '.master-badge']
    missing = [cl for cl in classes if cl not in c]

    ok = (n_style_total == n_style_head) and not missing and has_root
    status = '✅' if ok else '⚠️'
    extra = f'缺:{missing}' if missing else ''
    print(f'{vol:26s} | {n_style_total:>3d} | {n_script:>3d} | {n_vars:>4d} | {n_media:>3d} | {status} {extra}')
