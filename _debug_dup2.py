# -*- coding: utf-8 -*-
"""检查 marxism 重复段落详情"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 找 "毛泽东面对的是" 的所有出现位置和上下文
print('=== "毛泽东面对的是" 出现位置 ===')
for m in re.finditer('毛泽东面对的是', c):
    start = m.start()
    # 提取该句子所在段落
    para_start = c.rfind('<p', 0, start)
    para_end = c.find('</p>', start)
    para = c[para_start:para_end+4]
    # 提取段落文本
    txt = re.sub(r'<[^>]+>', '', para)
    print(f'\n位置 {start}:')
    print(f'  文本: {txt.strip()[:150]}...')
    print(f'  段落完整长度: {len(para)}')

# 检查这些位置是否在同一section内
print('\n=== section 归属 ===')
sections = [(m.start(), m.group(0)) for m in re.finditer(r'<section[^>]*>', c)]
for m in re.finditer('毛泽东面对的是', c):
    pos = m.start()
    sec = [s for s in sections if s[0] < pos]
    if sec:
        last_sec = sec[-1]
        sec_id = re.search(r'id="([^"]*)"', last_sec[1])
        print(f'  位置{pos}: 位于 {sec_id.group(1) if sec_id else last_sec[1][:50]}')

# 对比两个位置的完整段落是否完全相同
print('\n=== 段落完全相同性 ===')
positions = [m.start() for m in re.finditer('毛泽东面对的是', c)]
paras = []
for start in positions:
    para_start = c.rfind('<p', 0, start)
    para_end = c.find('</p>', start)
    paras.append(c[para_start:para_end+4])

for i in range(len(paras)):
    for j in range(i+1, len(paras)):
        if paras[i] == paras[j]:
            print(f'  段落{i+1} 与 段落{j+1} 完全相同')
        else:
            # 计算相似度
            import difflib
            ratio = difflib.SequenceMatcher(None, paras[i], paras[j]).ratio()
            print(f'  段落{i+1} 与 段落{j+1} 相似度: {ratio:.2f}')