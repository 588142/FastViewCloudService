# -*- coding: utf-8 -*-
"""检查三个style块之间是否存在冲突的重复CSS定义"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

styles = re.findall(r'<style[^>]*>([\s\S]*?)</style>', c, re.I)
print('style块数:', len(styles))

# 收集每个选择器的定义（按块序号）
from collections import defaultdict
sel_rules = defaultdict(list)
for bi, css in enumerate(styles):
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        sel = m.group(1).strip()
        body = re.sub(r'\s+', ' ', m.group(2)).strip()
        # 跳过 @font-face / @media 内的重复（单独处理@media）
        sel_rules[sel].append((bi, body))

print()
print('=== 冲突定义（同一选择器在不同块中值不同） ===')
for sel, defs in sel_rules.items():
    if len(defs) > 1:
        vals = set(v for _, v in defs)
        if len(vals) > 1:
            print('选择器: {}'.format(sel[:60]))
            for bi, v in defs:
                print('   [块{}] {}'.format(bi + 1, v[:160]))
            print()

print('=== 影响版式的关键选择器 ===')
for sel in ['.shell', '.page', 'main', '.sec', ':root', 'body', '.masthead', 'footer']:
    if sel in sel_rules:
        for bi, v in sel_rules[sel]:
            print('[块{}] {} {{ {} }}'.format(bi + 1, sel, v[:180]))
