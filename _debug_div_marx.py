# -*- coding: utf-8 -*-
"""精确排查marxism-lineage的div不平衡：列出所有未闭合的div位置"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 去掉script/style内容避免误报
c_body = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL)
c_body = re.sub(r'<style.*?</style>', '', c_body, flags=re.DOTALL)

# 只追踪div
stack = []
events = []
for m in re.finditer(r'<(/?)(div)((?:\s[^>]*)?)(/?)>', c_body):
    closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) or '', m.group(4)
    if selfclose:
        continue
    line = c_body[:m.start()].count('\n') + 1
    if not closing:
        stack.append((m.start(), line, attrs[:60]))
        events.append((line, 'open', attrs[:60]))
    else:
        if stack:
            stack.pop()
        events.append((line, 'close', ''))

print(f'未闭合div: {len(stack)} 个')
for pos, line, attrs in stack:
    # 显示该div开标签附近的上下文
    ctx = c_body[pos:pos+200].replace('\n', ' ')
    print(f'  line {line}: <div {attrs[:50]}>  ctx: {ctx[:120]}')
