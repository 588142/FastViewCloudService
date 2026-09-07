# -*- coding: utf-8 -*-
"""在原始文件上追踪marxism-lineage未闭合div（已确认注释/script/style中无div干扰）"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

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
            # 多余的闭合
            line = c[:m.start()].count('\n') + 1
            print(f'⚠️ 多余 </div> @ line {line}')

print(f'未闭合div: {len(stack)} 个\n')
for pos, attrs in stack:
    line = c[:pos].count('\n') + 1
    print(f'===== <div {attrs}> @ line {line} =====')
    seg = c[pos:pos+500].replace('\n', ' ⏎ ')
    print(seg[:500])
    print()
