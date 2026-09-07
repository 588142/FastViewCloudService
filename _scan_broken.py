# -*- coding: utf-8 -*-
"""扫描桌面版目录页 + 各卷的断链"""
import os, re

dt = r'c:\Users\Admin1\Desktop\Trae资料库'

print('=== A. 目录页断链扫描 ===')
for f in ['index.html', '主题索引.html', '阅读指南.html', '人物索引.html']:
    fp = os.path.join(dt, '思想图谱系列', f)
    c = open(fp, encoding='utf-8').read()
    links = re.findall(r'href="(\.\.[^"]*)"', c)
    broken = []
    for l in links:
        full = os.path.normpath(os.path.join(os.path.dirname(fp), l))
        if not os.path.exists(full):
            broken.append(l)
    print('=== %s ===' % f)
    print('  跨链接总数: %d, 断链: %d' % (len(links), len(broken)))
    for b in broken[:15]:
        print('    断链: %s' % b)
    if len(broken) > 15:
        print('    ...共 %d 条' % len(broken))

print()
print('=== B. 各卷内部跨卷链接断链扫描 ===')
total_broken = 0
for d in os.listdir(dt):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    for f in os.listdir(dp):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        c = open(fp, encoding='utf-8').read()
        links = re.findall(r'href="(\.\.[^"]*)"', c)
        broken = [l for l in links if not os.path.exists(os.path.normpath(os.path.join(dp, l)))]
        if broken:
            total_broken += len(broken)
            print('  %s/%s: %d 断链' % (d, f, len(broken)))
            for b in broken[:3]:
                print('    -> %s' % b)
print()
print('=== 各卷断链总计: %d ===' % total_broken)