# -*- coding: utf-8 -*-
"""定位 marxism div 差异位置 + 主题索引版本差异"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
desktop = r'c:\Users\Admin1\Desktop\Trae资料库'

# 1. 定位 marxism 中缺少闭合的 div
print('=== marxism div 差异定位 ===')
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()
c_no_script = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL)
c_clean = re.sub(r'<!--.*?-->', '', c_no_script, flags=re.DOTALL)

# 使用栈跟踪div嵌套
# 找到所有div开/闭标签的位置
opens = [(m.start(), m.group(0)) for m in re.finditer(r'<div\b', c_clean)]
closes = [(m.start(), m.group(0)) for m in re.finditer(r'</div>', c_clean)]

print(f'开标签: {len(opens)}, 闭标签: {len(closes)}')

# 找出从哪个位置开始不平衡 - 用游标法模拟
# 对每段文本，先找最近的未闭合div的深度
# 简单方法：找第一处深度为负或开始持续不闭合的位置
depth = 0
first_neg = None
depth_history = []
all_tags = sorted(opens + closes, key=lambda x: x[0])
for pos, tag in all_tags:
    if tag.startswith('<div'):
        depth += 1
    else:
        depth -= 1
    depth_history.append((pos, tag, depth))
    if depth < 0 and first_neg is None:
        first_neg = (pos, tag, depth)
        break

if first_neg:
    print(f'第一个负深度位置: 字符{first_neg[0]}')
    # 找该位置的上下文
    ctx = c_clean[max(0, first_neg[0]-200):first_neg[0]+200]
    print(f'上下文: ...{ctx}...')
else:
    # 没有负深度，说明是结尾有多余的开标签
    print(f'没有负深度，最终深度={depth}')
    print(f'说明有 {depth} 个div未闭合')

    # 找最后几个未闭合的div
    # 重新模拟，记录每个开标签是否被匹配
    open_stack = []
    for pos, tag in all_tags:
        if tag.startswith('<div'):
            open_stack.append(pos)
        else:
            if open_stack:
                open_stack.pop()
    
    print(f'未闭合div位置: {len(open_stack)} 个')
    for p in open_stack[-10:]:
        ctx = c_clean[max(0,p-100):p+50]
        print(f'  位置{p}: ...{ctx}...')
        print()

print()
print('=== 主题索引版本对比 ===')
ws_fp = os.path.join(ws, '思想图谱系列', '主题索引.html')
dt_fp = os.path.join(desktop, '思想图谱系列', '主题索引.html')
wc = open(ws_fp, encoding='utf-8').read()
dc = open(dt_fp, encoding='utf-8').read()

# 提取标题结构对比
def extract_titles(c):
    return re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', c, re.DOTALL)

ws_titles = extract_titles(wc)
dt_titles = extract_titles(dc)
print(f'工作区标题数: {len(ws_titles)}, 桌面标题数: {len(dt_titles)}')
print(f'工作区前5标题: {[t.strip()[:30] for t in ws_titles[:5]]}')
print(f'桌面前5标题: {[t.strip()[:30] for t in dt_titles[:5]]}')

# 检查两边内容差异 - 用行数对比
ws_lines = wc.count('\n')
dt_lines = dc.count('\n')
print(f'工作区行数: {ws_lines}, 桌面行数: {dt_lines}')

# 检查桌面版是否缺少内容（比较人物链接等）
ws_links = set(re.findall(r'href="[^"]*"', wc))
dt_links = set(re.findall(r'href="[^"]*"', dc))
only_ws = ws_links - dt_links
only_dt = dt_links - ws_links
print(f'仅工作区有的链接: {len(only_ws)}')
for l in sorted(only_ws)[:5]:
    print(f'  {l[:80]}')
print(f'仅桌面有的链接: {len(only_dt)}')
for l in sorted(only_dt)[:5]:
    print(f'  {l[:80]}')