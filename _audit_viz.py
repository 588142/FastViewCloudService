# -*- coding: utf-8 -*-
"""全项目卷总检查：结构完整性 + 可视化（Three.js/Chart.js/Mermaid）"""
import os, re, glob, json

ROOT = r"c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列"

def walk_html():
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        if any(p in ('_shared', 'assets') for p in rel.split(os.sep)):
            continue
        for f in fn:
            if f.endswith('.html'):
                yield os.path.join(dp, f), os.path.relpath(os.path.join(dp, f), ROOT)

htmls = list(walk_html())
print(f"共 {len(htmls)} 个 HTML 文件\n")

stats = {'three': [], 'chart': [], 'mermaid': [], 'canvas': []}
for fp, rel in htmls:
    c = open(fp, encoding='utf-8').read()
    if 'three' in c.lower():
        stats['three'].append(rel)
    if 'chart.js' in c.lower() or 'chartjs' in c.lower() or 'Chart(' in c:
        stats['chart'].append(rel)
    if 'mermaid' in c.lower():
        stats['mermaid'].append(rel)
    if '<canvas' in c:
        stats['canvas'].append(rel)

for k, v in stats.items():
    print(f"== {k}: {len(v)} 个 ==")
    for r in v:
        print(f"   {r}")
