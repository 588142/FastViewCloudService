# -*- coding: utf-8 -*-
import os, re
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = [
    ('truth-dimensions', '真理的多维图景'),
    ('marxism-lineage', '马克思主义谱系'),
    ('economics-lineage', '经济思想谱系'),
    ('econ-part2-lineage', '经济思想谱系下篇'),
    ('psych-lineage', '心理学思想谱系'),
    ('math-lineage', '数学思想谱系'),
]

print(f'{"卷宗":15s} | {"大小":>5s} | {"行数":>5s} | {"汉字":>6s} | {"附录":>6s} | {"3D":>3s} | {"图":>3s} | {"动画":>4s}')
print('-' * 65)

total_zh = 0
total_lines = 0
for wd, cn in vols:
    fp = os.path.join(ws, wd, wd + '.html')
    c = open(fp, encoding='utf-8').read()
    lines = c.count('\n') + 1
    zh = len(re.findall(r'[\u4e00-\u9fff]', c))
    appx = len(re.findall(r'id="appendix-[a-k]"', c))
    has_3d = 'three.min.js' in c
    has_chart = 'chart.js' in c
    has_anim = 'animation' in c.lower() or 'animate' in c.lower()
    size = os.path.getsize(fp) // 1024
    total_zh += zh
    total_lines += lines
    print(f'{cn:15s} | {size:>3}KB | {lines:>4}行 | {zh:>5}字 | {appx:>2}/11 | {int(has_3d):>2} | {int(has_chart):>2} | {int(has_anim):>2}')

print(f'\n合计: 6卷, {total_lines}行, {total_zh}汉字')
print(f'升级前size: 59+75+164+83+125+85 = 591KB')
print(f'升级后size: 131+155+233+160+196+158 = 1033KB')
print(f'净增: 442KB (+75%)')