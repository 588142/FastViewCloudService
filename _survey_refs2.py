# -*- coding: utf-8 -*-
"""检查目录页与根级页面的 _shared 引用"""
import os, re

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'

def refs_of(c):
    out = []
    out += re.findall(r'(?:src|href)="([^"]*_shared[^"]*)"', c)
    out += re.findall(r"url\(['\"]?([^'\"()]*_shared[^'\"()]*)['\"]?\)", c)
    return set(out)

base = os.path.join(ROOT, '思想图谱系列')
print('=== 思想图谱系列 根级（非卷内）html ===')
for f in sorted(os.listdir(base)):
    if not f.endswith('.html'):
        continue
    p = os.path.join(base, f)
    r = refs_of(open(p, encoding='utf-8').read())
    if r:
        print(f, '->', r)

print('=== 根目录非下划线前缀 html ===')
for f in sorted(os.listdir(ROOT)):
    if not f.endswith('.html') or f.startswith('_'):
        continue
    p = os.path.join(ROOT, f)
    r = refs_of(open(p, encoding='utf-8').read())
    if r:
        print(f, '->', r)

print('=== 根目录散件（_前缀）的字体类引用（非 ./_shared/ 前缀）===')
for f in sorted(os.listdir(ROOT)):
    if not f.endswith('.html') or not f.startswith('_'):
        continue
    p = os.path.join(ROOT, f)
    c = open(p, encoding='utf-8').read()
    r = set(re.findall(r"url\(['\"]?([^'\"()]*_shared[^'\"()]*)['\"]?\)", c))
    odd = [x for x in r if not x.startswith('./_shared/')]
    if odd:
        print(f, '->', odd)
