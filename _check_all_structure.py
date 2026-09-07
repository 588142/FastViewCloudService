# -*- coding: utf-8 -*-
"""检查所有标星卷的多重</html>问题 + section平级性"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

print('=== 多重文档框架检查 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    html_cnt = len(re.findall(r'</html>', c))
    body_cnt = len(re.findall(r'<body', c))
    dt_cnt = len(re.findall(r'<!DOCTYPE', c, re.IGNORECASE))
    print(f'{vol}: </html>={html_cnt}, <body>={body_cnt}, DOCTYPE={dt_cnt}')

print('\n=== section 平级性检查 (marxism) ===')
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()
# 用简单深度法检查section嵌套
depth = 0
nested = False
for m in re.finditer(r'<section\b|</section>', c):
    if m.group(0).startswith('<section'):
        depth += 1
        if depth > 1:
            nested = True
            print(f'  section嵌套 @ {m.start()}')
    else:
        depth -= 1
print(f'  最终深度: {depth}, 有嵌套: {nested}')

print('\n=== 各模块 section 数量 ===')
# 按位置分段统计
segments = [
    ('基础内容', 7911, 48666),
    ('本科附录', 51951, 99647),
    ('硕士模块', 104745, 136655),
    ('博士模块', 142379, 199670),
]
for name, start, end in segments:
    seg = c[start:end]
    opens = len(re.findall(r'<section\b', seg))
    closes = len(re.findall(r'</section>', seg))
    print(f'  {name}: {opens}开/{closes}闭')

# 检查是否有 main/nav 等结构标签
print('\n=== main/nav 结构标签 ===')
for t in ['<main', '</main>', '<nav', '</nav>']:
    poses = [m.start() for m in re.finditer(re.escape(t), c)]
    print(f'  {t}: {poses}')