# -*- coding: utf-8 -*-
"""最终验证：桌面同步 + HTML结构完整性"""
import os, re, glob

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

star_vols = [
    ('truth-dimensions', '真理的多维图景'),
    ('marxism-lineage', '马克思主义谱系'),
    ('economics-lineage', '经济思想谱系'),
    ('econ-part2-lineage', '经济思想谱系下篇'),
    ('psych-lineage', '心理学思想谱系'),
    ('math-lineage', '数学思想谱系'),
    ('logic-lineage', '逻辑与论证思想谱系'),
]

print('=== 1. 桌面同步验证（7个标星卷） ===')
for en, cn in star_vols:
    wf = os.path.join(ws, en, en + '.html')
    if not os.path.exists(wf):
        print(f'  !! 工作区文件缺失: {en}')
        continue
    w_size = os.path.getsize(wf)
    with open(wf, encoding='utf-8') as f:
        w_zh = len(f.read())
    results = []
    for fname in [en + '.html', cn + '.html']:
        df = os.path.join(dt, cn, fname)
        if os.path.exists(df):
            with open(df, encoding='utf-8') as f:
                d_zh = len(f.read())
            match = 'OK' if d_zh == w_zh else 'MISMATCH'
            results.append('{}:{}'.format(fname, match))
        else:
            results.append('{}:MISSING'.format(fname))
    print('  {:22s} {:4d}KB  {}'.format(en, w_size // 1024, '; '.join(results)))

print()
print('=== 2. HTML结构完整性（7个标星卷） ===')
for en, cn in star_vols:
    wf = os.path.join(ws, en, en + '.html')
    with open(wf, encoding='utf-8') as f:
        c = f.read()
    checks = {}
    checks['DOCTYPE'] = 'OK' if c.count('<!DOCTYPE') == 1 else 'x{}'.format(c.count('<!DOCTYPE'))
    checks['html标签'] = 'OK' if c.count('<html') == 1 and c.count('</html>') == 1 else 'x'
    checks['head'] = 'OK' if c.count('<head>') == 1 and c.count('</head>') == 1 else 'x'
    checks['body'] = 'OK' if c.count('<body') == 1 and c.count('</body>') == 1 else 'x'
    # div平衡
    div_open = len(re.findall(r'<div[\s>]', c))
    div_close = c.count('</div>')
    checks['div({}/{})'.format(div_open, div_close)] = 'OK' if div_open == div_close else '!!'
    # 图片引用
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', c)
    broken_imgs = 0
    for src in imgs:
        if src.startswith('http'):
            continue
        p = os.path.normpath(os.path.join(ws, en, src))
        if not os.path.exists(p):
            broken_imgs += 1
    checks['图片({}处)'.format(len(imgs))] = 'OK' if broken_imgs == 0 else '{}断'.format(broken_imgs)
    # 跨卷链接
    cross = re.findall(r'href="\.\./([^"]*)"', c)
    broken_cross = 0
    for cl in cross:
        full = os.path.normpath(os.path.join(ws, en, '..', cl))
        if not os.path.exists(full):
            broken_cross += 1
    checks['跨卷链接({})'.format(len(cross))] = 'OK' if broken_cross == 0 else '{}断'.format(broken_cross)
    status = 'PASS' if all(v == 'OK' for v in checks.values()) else 'FAIL'
    print('  [{}] {}'.format(status, en))
    for k, v in checks.items():
        if v != 'OK':
            print('        ! {}: {}'.format(k, v))

print()
print('=== 3. 桌面版链接验证（7个标星卷） ===')
for en, cn in star_vols:
    for fname in [en + '.html', cn + '.html']:
        df = os.path.join(dt, cn, fname)
        if not os.path.exists(df):
            continue
        with open(df, encoding='utf-8') as f:
            c = f.read()
        cross = re.findall(r'href="\.\./([^"]*)"', c)
        broken = 0
        for cl in cross:
            full = os.path.normpath(os.path.join(dt, cn, '..', cl))
            if not os.path.exists(full):
                broken += 1
        mark = 'OK' if broken == 0 else '{}断'.format(broken)
        print('  {:14s} {:<28s} 跨卷{}个 [{}]'.format(cn, fname, len(cross), mark))

print()
print('=== 4. 阅读指南/目录页同步 ===')
for fname in ['index.html', '阅读指南.html', '主题索引.html']:
    wf = os.path.join(ws, '思想图谱系列', fname)
    df = os.path.join(dt, '思想图谱系列', fname)
    if os.path.exists(wf) and os.path.exists(df):
        with open(wf, encoding='utf-8') as f:
            a = f.read()
        with open(df, encoding='utf-8') as f:
            b = f.read()
        print('  {}: {}'.format(fname, 'OK' if a == b else 'DIFF!!'))
    else:
        print('  {}: 缺失 (ws={}, dt={})'.format(fname, os.path.exists(wf), os.path.exists(df)))
