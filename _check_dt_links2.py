# -*- coding: utf-8 -*-
"""验证桌面版 思想图谱系列 全部页面链接的真实断链"""
import os, re

dt = r'c:\Users\Admin1\Desktop\Trae资料库'
base = os.path.join(dt, '思想图谱系列')

for fname in ['index.html', '阅读指南.html', '主题索引.html']:
    fp = os.path.join(base, fname)
    c = open(fp, encoding='utf-8').read()
    links = re.findall(r'href="\.\./([^"]*)"', c)
    broken = []
    for l in sorted(set(links)):
        full = os.path.normpath(os.path.join(base, '..', l))
        if not os.path.exists(full):
            broken.append(l)
    print('{}: 链接{}个(去重后{}), 断链{}个'.format(fname, len(links), len(set(links)), len(broken)))
    for b in broken:
        print('    BROKEN -> ../{}'.format(b))
    print()
