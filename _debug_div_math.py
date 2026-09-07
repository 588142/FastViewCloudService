# -*- coding: utf-8 -*-
"""检查math-lineage的div平衡"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'math-lineage', 'math-lineage.html')
c = open(fp, encoding='utf-8').read()

# 确认div是否在注释/script/style中
comments = re.findall(r'<!--.*?-->', c, re.DOTALL)
scripts = re.findall(r'<script.*?</script>', c, re.DOTALL)
styles = re.findall(r'<style.*?</style>', c, re.DOTALL)
print(f'注释: {len(comments)}, script: {len(scripts)}, style: {len(styles)}')
div_in_comment = sum('</div>' in cm or '<div' in cm for cm in comments)
div_in_script = sum('</div>' in cm or '<div' in cm for cm in scripts)
div_in_style = sum('</div>' in cm or '<div' in cm for cm in styles)
print(f'注释含div: {div_in_comment}, script含div: {div_in_script}, style含div: {div_in_style}')

d_open = len(re.findall(r'<div(?:\s[^>]*)?>', c))
d_close = len(re.findall(r'</div>', c))
print(f'<div>={d_open} </div>={d_close} 差={d_open-d_close}')

# 在原始文件上追踪未闭合div
stack = []
for m in re.finditer(r'<(/?)(div)((?:\s[^>]*)?)(/?)>', c):
    closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) or '', m.group(4)
    if selfclose:
        continue
    if not closing:
        stack.append((m.start(), attrs.strip()[:70]))
    else:
        if stack:
            stack.pop()
        else:
            line = c[:m.start()].count('\n') + 1
            print(f'⚠️ 多余 </div> @ line {line}')

print(f'未闭合div: {len(stack)}')
for pos, attrs in stack:
    line = c[:pos].count('\n') + 1
    print(f'  @line {line}: <div {attrs}>')
    print(f'    {c[pos:pos+300].replace(chr(10), " ⏎ ")[:300]}')
