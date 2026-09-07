# -*- coding: utf-8 -*-
"""补丁：为缺失 mermaid.min.js 的卷补齐本地副本（依据 HTML 中的 ./_shared/js/mermaid.min.js 引用）。"""
import os, shutil, re

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'
SRC = os.path.join(ROOT, '_shared', 'js', 'mermaid.min.js')  # 脚本上一轮已复制到根 _shared

missing = []
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        c = open(p, encoding='utf-8').read()
        if './_shared/js/mermaid.min.js' not in c:
            continue
        d = os.path.dirname(p)
        dst = os.path.join(d, '_shared', 'js', 'mermaid.min.js')
        if not os.path.exists(dst):
            missing.append((p, dst))

for p, dst in missing:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(SRC, dst)
    print('补齐:', os.path.relpath(dst, ROOT))

print(f'=== 共补齐 {len(missing)} 个 ===')

# 复检所有本地引用存在性
bad = 0
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        c = open(p, encoding='utf-8').read()
        for m in re.finditer(r'src="(\./_shared/js/[^"]+)"', c):
            t = os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))
            if not os.path.exists(t):
                print('MISSING:', os.path.relpath(p, ROOT), '->', m.group(1))
                bad += 1
print(f'=== 本地引用缺失: {bad} 个 ===')
