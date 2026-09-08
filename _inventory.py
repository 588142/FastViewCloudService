# -*- coding: utf-8 -*-
"""继续去重前盘点：重复文件、_export、.bak、IDE 缓存、各卷 assets 体积"""
import os, hashlib, collections

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'

def dir_size(d):
    if not os.path.isdir(d):
        return 0
    return sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(d) for f in fn)

# 1. 各类占用
print('=== 占用盘点 ===')
for name, d in [
    ('_export', os.path.join(ROOT, '_export')),
    ('_dl', os.path.join(ROOT, '_dl')),
    ('.trae-html-share-packages', os.path.join(ROOT, '.trae-html-share-packages')),
    ('_shared(根)', os.path.join(ROOT, '_shared')),
    ('_shared(中文站)', os.path.join(ROOT, '思想图谱系列', '_shared')),
    ('.git', os.path.join(ROOT, '.git')),
]:
    print(f'  {name:24s} {dir_size(d)/1048576:8.1f} MB')

# 2. .bak 文件
baks = [(os.path.relpath(os.path.join(dp, f), ROOT), os.path.getsize(os.path.join(dp, f)))
        for dp, dn, fn in os.walk(ROOT)
        for f in fn if f.endswith('.bak')]
print(f'.bak 文件: {len(baks)} 个, 共 {sum(s for _, s in baks)/1048576:.1f} MB')

# 3. 重复文件（按大小分组的哈希检测，只查 >100KB 的文件）
by_size = collections.defaultdict(list)
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dp or '__pycache__' in dp:
        continue
    for f in fn:
        p = os.path.join(dp, f)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        if sz > 102400:
            by_size[sz].append(p)

dup_groups = []
for sz, files in by_size.items():
    if len(files) < 2:
        continue
    by_hash = collections.defaultdict(list)
    for p in files:
        h = hashlib.md5(open(p, 'rb').read(1048576)).hexdigest()
        by_hash[h].append(p)
    for h, ps in by_hash.items():
        if len(ps) > 1:
            dup_groups.append(ps)

print(f'=== 重复大文件组 (>100KB, 同大小且同MD5前缀): {len(dup_groups)} 组 ===')
for g in sorted(dup_groups, key=lambda g: -os.path.getsize(g[0])):
    sz = os.path.getsize(g[0])
    total = sz * len(g)
    print(f'  {len(g):2d} x {sz/1048576:7.1f}MB = {total/1048576:7.1f}MB:')
    for p in g[:6]:
        print(f'     {os.path.relpath(p, ROOT)}')
    if len(g) > 6:
        print(f'     ... 另有 {len(g)-6} 个')
