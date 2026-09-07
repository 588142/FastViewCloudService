# -*- coding: utf-8 -*-
"""修复后终验：只验证div平衡、锚点、跨卷链接、样式（忽略SVG误报）"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

print(f'{"卷":26s} | {"div开/闭":>10s} | {"section":>3s} | {"锚点":>4s}/{"内链":>4s} | {"跨卷":>4s} | 状态')
all_ok = True
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()

    d_open = len(re.findall(r'<div(?:\s[^>]*)?>', c))
    d_close = len(re.findall(r'</div>', c))
    sections = len(re.findall(r'<section', c))
    anchors = set(re.findall(r'id="([^"]*)"', c))
    links = re.findall(r'href="#([^"]*)"', c)
    broken = [l for l in links if l not in anchors]
    cross = re.findall(r'href="(\.\./[^"]*)"', c)
    cross_bad = [cl for cl in cross if not os.path.exists(os.path.normpath(os.path.join(ws, vol, cl)))]

    issues = []
    if d_open != d_close: issues.append(f'div {d_open}/{d_close}')
    if broken: issues.append(f'锚点断链{len(broken)}:{broken[:2]}')
    if cross_bad: issues.append(f'跨卷断链{len(cross_bad)}:{cross_bad[:2]}')
    if 'var(--accent)' not in c: issues.append('缺--accent')
    if 'viewport' not in c: issues.append('缺viewport')
    # 文档框架完整性（精确匹配标签名，避免header前缀误报）
    for t, n in [('<!DOCTYPE', 1), ('<html', 1), ('</html>', 1), ('<head', 1), ('<body', 1), ('</body>', 1)]:
        if t.endswith('>'):
            pat = re.escape(t)
        else:
            pat = re.escape(t) + r'(?:\s[^>]*)?>'
        cnt = len(re.findall(pat, c, re.IGNORECASE))
        if cnt != n:
            issues.append(f'{t}x{cnt}')

    ok = not issues
    all_ok = all_ok and ok
    status = '✅' if ok else '⚠️'
    print(f'{vol:26s} | {d_open:>4d}/{d_close:<4d} | {sections:>3d} | {len(anchors):>4d}/{len(links):>4d} | {len(cross):>4d} | {status} {", ".join(issues)[:80]}')

print(f'\n{"全部通过 ✅" if all_ok else "存在问题 ⚠️"}')
