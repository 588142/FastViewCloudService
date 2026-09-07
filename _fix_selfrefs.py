# -*- coding: utf-8 -*-
"""修复卷内文件残留的 '带卷名自引用' 字体路径：./<卷名>/_shared/fonts/ -> ../_shared/fonts/"""
import os, re

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'

fixed = []
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        # 仅处理卷内文件（中文站卷内 / 英文站卷内）
        is_cn_vol = rel.startswith('思想图谱系列\\') and rel.count('\\') >= 2
        is_en_vol = rel.count('\\') == 1 and not rel.startswith('_') and not rel.startswith('思想图谱系列')
        if not (is_cn_vol or is_en_vol):
            continue
        c = open(p, encoding='utf-8').read()
        orig = c
        c = re.sub(r'\./[^/"\'()]+/_shared/fonts/', '../_shared/fonts/', c)
        if c != orig:
            open(p, 'w', encoding='utf-8').write(c)
            fixed.append(rel)

print(f'修复 {len(fixed)} 个文件')
for f in fixed:
    print('  F:', f)
