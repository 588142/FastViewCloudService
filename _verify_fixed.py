# -*- coding: utf-8 -*-
"""修复后综合验证：div平衡、锚点、样式、脚本、跨卷链接"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param',
        'source','track','wbr'}

def check_balance(c):
    stack = []
    problems = []
    for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\s[^<>]*)?)(/?)>', c):
        closing, tag, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3) or '', m.group(4)
        if tag in VOID or selfclose:
            continue
        if tag in ('!--', '!DOCTYPE', 'script', 'style'):
            continue
        if not closing:
            stack.append((tag, m.start()))
        else:
            if stack and stack[-1][0] == tag:
                stack.pop()
            else:
                problems.append(f'line@{m.start()}: 期望闭合</{stack[-1][0] if stack else "?"}> 却遇</{tag}>')
    for tag, pos in stack:
        problems.append(f'未闭合: <{tag}>@{pos}')
    return problems

print(f'{"卷":26s} | {"div开":>4s}/{"div闭":>4s} | {"section":>3s} | {"锚点":>4s}/{"内链":>4s} | {"跨卷":>4s} | div平衡')
all_ok = True
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()

    div_open = len(re.findall(r'<div(?:\s[^>]*)?>', c))
    div_close = len(re.findall(r'</div>', c))
    sections = len(re.findall(r'<section', c))
    anchors = set(re.findall(r'id="([^"]*)"', c))
    links = re.findall(r'href="#([^"]*)"', c)
    broken = [l for l in links if l not in anchors]
    cross = re.findall(r'href="(\.\./[^"]*)"', c)
    cross_bad = [cl for cl in cross if not os.path.exists(os.path.normpath(os.path.join(ws, vol, cl)))]

    prob = check_balance(c)
    # 排除script/style内的伪标签（含JS字符串里的</div>等），粗查
    c_body = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL)
    c_body = re.sub(r'<style.*?</style>', '', c_body, flags=re.DOTALL)
    prob2 = check_balance(c_body)

    issues = []
    if div_open != div_close: issues.append(f'div {div_open}/{div_close}')
    if prob2: issues.append(f'不平衡: {prob2[:3]}')
    if broken: issues.append(f'锚点断链{len(broken)}: {broken[:3]}')
    if cross_bad: issues.append(f'跨卷断链{len(cross_bad)}: {cross_bad[:2]}')
    # 样式完整性
    for v in ['--bg','--ink','--accent','--font-head']:
        if f'var({v})' not in c: issues.append(f'缺{v}')
    if 'max-width' not in c: issues.append('缺max-width')
    if 'viewport' not in c: issues.append('缺viewport')

    ok = not issues
    all_ok = all_ok and ok
    status = '✅' if ok else '⚠️'
    print(f'{vol:26s} | {div_open:>4d}/{div_close:>4d} | {sections:>3d} | {len(anchors):>4d}/{len(links):>4d} | {len(cross):>4d} | {status} {", ".join(issues)[:100]}')

print(f'\n{"全部通过 ✅" if all_ok else "存在问题 ⚠️"}')
