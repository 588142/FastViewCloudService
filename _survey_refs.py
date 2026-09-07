# -*- coding: utf-8 -*-
"""调查 mermaid/字体/three/chart 在 HTML 中的引用格式"""
import os, re, collections

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'
mermaid_refs = collections.Counter()
font_refs = collections.Counter()
js_refs = collections.Counter()

for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        c = open(p, encoding='utf-8').read()
        for m in re.finditer(r'src="([^"]*mermaid[^"]*)"', c):
            mermaid_refs[m.group(1)] += 1
        for m in re.finditer(r"url\(\s*['\"]?([^'\"()]+\.(?:ttf|woff2?))['\"]?\s*\)", c):
            font_refs[m.group(1)] += 1
        for m in re.finditer(r'src="([^"]*(?:three\.min|chart\.umd|OrbitControls|echarts)[^"]*)"', c):
            js_refs[m.group(1)] += 1

print('=== mermaid 引用格式 ===')
for k, v in mermaid_refs.items():
    print(f'{v:3d} x  {k}')
print('=== three/chart/orbit/echarts 引用格式 ===')
for k, v in js_refs.items():
    print(f'{v:3d} x  {k}')
print('=== 字体引用格式 ===')
for k, v in font_refs.most_common(30):
    print(f'{v:3d} x  {k}')
print(f'字体引用总条数: {sum(font_refs.values())}, 去重后样式: {len(font_refs)}')
