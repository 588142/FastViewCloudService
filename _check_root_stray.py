# -*- coding: utf-8 -*-
"""检查桌面版是否有页面引用根目录游离文件"""
import os, re, glob

dt = r'c:\Users\Admin1\Desktop\Trae资料库'
root_files = ['index.html', '主题索引.html', '人物索引.html', '阅读指南.html']

# 统计所有html中的链接，找指向根目录这些文件的引用
refs = {f: [] for f in root_files}
for hf in glob.glob(os.path.join(dt, '**', '*.html'), recursive=True):
    try:
        c = open(hf, encoding='utf-8').read()
    except Exception:
        continue
    base = os.path.dirname(hf)
    for m in re.finditer(r'href="([^"#]+?\.html)"', c):
        href = m.group(1)
        if href.startswith(('http', 'mailto')):
            continue
        full = os.path.normpath(os.path.join(base, href))
        for rf in root_files:
            if os.path.normpath(full) == os.path.normpath(os.path.join(dt, rf)):
                refs[rf].append(os.path.relpath(hf, dt))

for rf in root_files:
    rl = refs[rf]
    print('{:<16s} 被引用 {} 处'.format(rf, len(rl)))
    for r in rl[:10]:
        print('    <-', r)
print()
# 这些根文件自身的断链情况
for rf in root_files:
    fp = os.path.join(dt, rf)
    if not os.path.exists(fp):
        continue
    c = open(fp, encoding='utf-8').read()
    base = os.path.dirname(fp)
    broken = []
    for m in re.finditer(r'href="\.\.?/([^"#]+?\.html)"', c):
        href = m.group(1)
        full = os.path.normpath(os.path.join(base, href))
        if not os.path.exists(full):
            broken.append(href)
    old = [o for o in ['econ-thought.html', 'art-aesthetics.html', 'eastern-thought.html', 'edu-lineage.html'] if o in c]
    print('{}: 断链{}个, 旧名引用{}个'.format(rf, len(broken), len(old)))
