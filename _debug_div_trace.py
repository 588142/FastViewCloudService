# -*- coding: utf-8 -*-
"""追踪marxism-lineage未闭合div：显示每个未闭合div的内容区间"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

c_clean = re.sub(r'<!--.*?-->', '', c, flags=re.DOTALL)
c_clean = re.sub(r'<script.*?</script>', '', c_clean, flags=re.DOTALL)
c_clean = re.sub(r'<style.*?</style>', '', c_clean, flags=re.DOTALL)

# 栈：记录 div 的 (位置, 行号, attrs)
stack = []
# 记录每个div的闭合情况
for m in re.finditer(r'<(/?)(div)((?:\s[^>]*)?)(/?)>', c_clean):
    closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) or '', m.group(4)
    if selfclose:
        continue
    line = c_clean[:m.start()].count('\n') + 1
    if not closing:
        stack.append((m.start(), line, attrs.strip()[:80]))
    else:
        if stack:
            stack.pop()
        # 不匹配的情况先忽略，只关心最终未闭合的

print(f'未闭合div: {len(stack)} 个\n')
for pos, line, attrs in stack:
    # 找这个div之后第一个非div闭合标签（确定它的"应该闭合点"）
    after = c_clean[pos:]
    # 找下一个同层级的闭合标签
    closes = [mm for mm in re.finditer(r'</(?:section|article|main|body|html)>', after)]
    end_pos = closes[0].start() + pos if closes else len(c_clean)
    # 显示该div到结束点的内容（取中间部分）
    seg = c_clean[pos:min(end_pos, pos+600)]
    # 找seg里的特征：是否包含明显的"内容结束"标记
    lines = seg.split('\n')
    close_tag = closes[0].group(0) if closes else 'EOF'
    print(f'--- line {line}: <div {attrs}>')
    print(f'    内容区间到: line {c_clean[:end_pos].count(chr(10))+1} (最近的{close_tag})')
    print(f'    内容前150字: {seg[:150].replace(chr(10), " ")}')
    print()
