# -*- coding: utf-8 -*-
"""用绝对位置查看未闭合div的完整上下文（原始文件）"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

c_clean = re.sub(r'<!--.*?-->', '', c, flags=re.DOTALL)
c_clean = re.sub(r'<script.*?</script>', '', c_clean, flags=re.DOTALL)
c_clean = re.sub(r'<style.*?</style>', '', c_clean, flags=re.DOTALL)

stack = []
for m in re.finditer(r'<(/?)(div)((?:\s[^>]*)?)(/?)>', c_clean):
    closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) or '', m.group(4)
    if selfclose:
        continue
    if not closing:
        stack.append((m.start(), attrs.strip()[:60]))
    else:
        if stack:
            stack.pop()

for pos, attrs in stack:
    line = c[:pos].count('\n') + 1
    print(f'===== <div {attrs}> @ 原始行 {line} =====')
    # 打印该div开始后 400 字符
    seg = c[pos:pos+400]
    print(seg[:400].replace('\n', ' ⏎ '))
    print()
