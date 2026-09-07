# -*- coding: utf-8 -*-
"""P1 后验证：残留 _shared 检查 + 全部相对引用存在性检查 + 体积统计"""
import os, re

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'

# 1. 残留卷内 _shared
left = []
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for d in dn:
        if d == '_shared':
            full = os.path.join(dp, d)
            if full not in (os.path.join(ROOT, '_shared'), os.path.join(ROOT, '思想图谱系列', '_shared')):
                left.append(os.path.relpath(full, ROOT))
print(f'残留卷内 _shared: {len(left)} 个')
for l in left[:10]:
    print('  !', l)

# 2. 相对引用存在性
PAT = re.compile(r'(?:src|href)="((?:\.{1,2}/)[^"]+)"')
PAT_URL = re.compile(r"url\(['\"]?((?:\.{1,2}/)[^'\"()]+)['\"]?\)")
bad = []
n_ref = 0
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        c = open(p, encoding='utf-8').read()
        refs = PAT.findall(c) + PAT_URL.findall(c)
        base = os.path.dirname(p)
        for r in refs:
            n_ref += 1
            t = os.path.normpath(os.path.join(base, r))
            if not os.path.exists(t):
                bad.append((os.path.relpath(p, ROOT), r))
print(f'相对引用总数: {n_ref}, 缺失: {len(bad)}')
for b in bad:
    print('  MISSING:', b[0], '->', b[1])

# 3. 体积统计
def dir_size(d):
    return sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(d) for f in fn)
total = dir_size(ROOT) - dir_size(os.path.join(ROOT, '.git'))
print(f'工作区内容总大小（不含 .git）: {total/1048576:.1f} MB')
for tag, d in [('根 _shared', os.path.join(ROOT, '_shared')),
               ('中文站 _shared', os.path.join(ROOT, '思想图谱系列', '_shared'))]:
    if os.path.isdir(d):
        print(f'  {tag}: {dir_size(d)/1048576:.1f} MB')
