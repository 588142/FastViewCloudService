# -*- coding: utf-8 -*-
"""提取 marxism 所有 script 块"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

print('=== 所有 script 块 ===')
for m in re.finditer(r'<script[^>]*>.*?</script>', c, re.DOTALL):
    s = m.group(0)
    src = re.search(r'src="([^"]*)"', s)
    if src:
        print(f'  @{m.start():>7}  src={src.group(1)}')
    else:
        # 内联脚本：取开头
        content = re.sub(r'<script[^>]*>', '', s)
        content = re.sub(r'</script>', '', content).strip()
        first_line = content.split('\n')[0][:80]
        print(f'  @{m.start():>7}  内联: {first_line}')

# 也要找自闭合script标签
print('\n=== 自闭合 script 标签 ===')
for m in re.finditer(r'<script[^>]*src="[^"]*"[^>]*/>', c):
    print(f'  @{m.start()}: {m.group(0)[:100]}')