# -*- coding: utf-8 -*-
"""排查所有 html 的 <script> 块内是否混入 HTML 注释（<!-- ... -->）"""
import os, re

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'
bad = []
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        c = open(p, encoding='utf-8').read()
        for m in re.finditer(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', c, flags=re.S | re.I):
            body = m.group(1)
            for cm in re.finditer(r'<!--.*?-->', body, flags=re.S):
                line_no = c[:m.start() + cm.start()].count('\n') + 1
                bad.append((os.path.relpath(p, ROOT), line_no, cm.group(0)[:60]))
print(f'发现 script 内 HTML 注释: {len(bad)} 处')
for b in bad:
    print(' ', b[0], f'L{b[1]}', b[2])
