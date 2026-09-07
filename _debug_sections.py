# -*- coding: utf-8 -*-
"""完整分析 marxism 中4个重复块的section结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 提取这4个位置所在 section 的完整内容
sections = []
for m in re.finditer(r'<section[^>]*>', c):
    sections.append((m.start(), m.group(0)))

print(f'总section数: {len(sections)}')
for idx, (pos, tag) in enumerate(sections):
    sec_id = re.search(r'id="([^"]*)"', tag)
    print(f'  section {idx}: id={sec_id.group(1) if sec_id else "?"} @ {pos}')

# 对每个重复位置，找到它所在section的完整结构
positions = [m.start() for m in re.finditer('毛泽东面对的是', c)]
for p in positions:
    # 找所在section
    sec_idx = None
    for i, (spos, stag) in enumerate(sections):
        if spos < p:
            sec_idx = i
        else:
            break
    if sec_idx is not None:
        sec_start = sections[sec_idx][0]
        # section结束 = 下一个section开始或文件尾
        if sec_idx + 1 < len(sections):
            sec_end = sections[sec_idx+1][0]
        else:
            sec_end = len(c)
        sec_content = c[sec_start:sec_end]
        # 找section内的标题
        heads = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', sec_content, re.DOTALL)
        print(f'\n位置{p} -> section {sec_idx} ({sections[sec_idx][1][:60]}...)')
        print(f'  section长度: {len(sec_content)}')
        print(f'  标题: {[h.strip()[:30] for h in heads]}')
        # 统计该section内"三大来源"段落出现次数
        cnt = sec_content.count('英国古典政治经济学')
        print(f'  该section内"英国古典政治经济学"次数: {cnt}')