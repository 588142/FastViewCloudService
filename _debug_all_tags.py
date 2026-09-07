# -*- coding: utf-8 -*-
"""列出 marxism 文件所有关键标签"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

print(f'文件总长: {len(c)}')

tags = ['<!DOCTYPE', '<html', '</html>', '<head', '</head>', '<body', '</body>',
        '<style', '</style>', '<article', '</article>', '<div class="shell"',
        '<footer', '</footer>']

all_pos = []
for t in tags:
    for m in re.finditer(re.escape(t), c):
        all_pos.append((m.start(), t))

all_pos.sort()
print(f'共 {len(all_pos)} 个标记\n')

for pos, t in all_pos:
    # 显示该标签前60字符（取最近的非空白文本）
    ctx = c[max(0,pos-60):pos]
    ctx_clean = re.sub(r'\s+', ' ', ctx)[-50:]
    print(f'  {pos:>7}  {t:15s} | ...{ctx_clean}')