# -*- coding: utf-8 -*-
"""检查主 head 内容结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 主head: @69 - @7903
head = c[69:7903]
print(f'主head长度: {len(head)}')

# 提取 head 内元素
print('\n=== head 内 meta ===')
for m in re.finditer(r'<meta[^>]*>', head):
    print(f'  {m.group(0)[:100]}')

print('\n=== head 内 title ===')
for m in re.finditer(r'<title>.*?</title>', head, re.DOTALL):
    print(f'  {m.group(0)[:100]}')

print('\n=== head 内 style 块 ===')
for m in re.finditer(r'<style[^>]*>.*?</style>', head, re.DOTALL):
    print(f'  @{m.start()}: 长度 {len(m.group(0))}')

print('\n=== head 内 script ===')
for m in re.finditer(r'<script[^>]*>.*?</script>', head, re.DOTALL):
    print(f'  @{m.start()}: {m.group(0)[:120]}')
for m in re.finditer(r'<script[^>]*src="[^"]*"[^>]*/?>', head):
    print(f'  @{m.start()}: {m.group(0)[:120]}')

print('\n=== head 内其他 ===')
# 看head的开头和结尾
print('head开头300字符:')
print(head[:300])
print('\nhead结尾300字符:')
print(head[-300:])