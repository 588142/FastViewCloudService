# -*- coding: utf-8 -*-
"""全36卷最终结构校验：单一框架 + div平衡 + 图片 + 锚点"""
import os, re

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

vol_dirs = [d for d in os.listdir(ws)
            if os.path.isdir(os.path.join(ws, d))
            and not d.startswith('_') and not d.startswith('.')
            and d not in ('思想图谱系列', 'series-overview')]

print('卷数: {}'.format(len(vol_dirs)))
print()
print('{:<26s} {:<6s} {:<6s} {:<6s} {:<6s} {:<6s} {:<8s}'.format(
    '卷', '框架', 'div', '图片', '内链', '锚点', '状态'))

def check(hf):
    c = open(hf, encoding='utf-8').read()
    base = os.path.dirname(hf)
    frame_ok = (c.count('<!DOCTYPE') == 1 and c.count('<html') == 1
                and c.count('</html>') == 1 and c.count('<head>') == 1
                and c.count('<body') == 1 and c.count('</body>') == 1)
    do = len(re.findall(r'<div[\s>]', c))
    dc = c.count('</div>')
    div_ok = (do == dc)
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', c)
    broken_img = sum(1 for s in imgs if not s.startswith('http')
                     and not os.path.exists(os.path.normpath(os.path.join(base, s))))
    # 内部锚点
    ids = set(re.findall(r'id="([^"]+)"', c))
    anchors = re.findall(r'href="#([^"]+)"', c)
    broken_anchor = sum(1 for a in anchors if a not in ids)
    # 同卷链接
    same_links = re.findall(r'href="([^"#]+?\.html)"', c)
    broken_same = sum(1 for l in same_links
                      if not l.startswith(('http', '../'))
                      and not os.path.exists(os.path.normpath(os.path.join(base, l))))
    return frame_ok, div_ok, broken_img, broken_same, broken_anchor, (len(imgs), do)

issues = []
for d in sorted(vol_dirs):
    mf = os.path.join(ws, d, d + '.html')
    if not os.path.exists(mf):
        mf2 = os.path.join(ws, d, d.replace('-lineage', '') + '.html')
        mf = mf2 if os.path.exists(mf2) else None
    if not mf:
        # 特殊名
        for f in os.listdir(os.path.join(ws, d)):
            if f.endswith('.html') and not f.startswith('_'):
                mf = os.path.join(ws, d, f)
                break
    if not mf:
        print('  !! {} 无主HTML'.format(d))
        continue
    fo, dv, bi, bs, ba, (ni, nd) = check(mf)
    ok = fo and dv and bi == 0 and bs == 0 and ba == 0
    status = 'PASS' if ok else 'FAIL'
    print('{:<26s} {:<6s} {:<6s} {:<6s} {:<6s} {:<6s} [{}]'.format(
        d, 'OK' if fo else 'x', 'OK' if dv else '{}≠{}'.format(nd, 'x'),
        str(bi), str(bs), str(ba), status))
    if not ok:
        issues.append((d, fo, dv, bi, bs, ba))

print()
print('=== 问题汇总 ===')
if issues:
    for d, fo, dv, bi, bs, ba in issues:
        print('  {}: frame={} div={} img断={} 同卷断={} 锚点断={}'.format(
            d, fo, dv, bi, bs, ba))
else:
    print('  全部36卷结构完整')
