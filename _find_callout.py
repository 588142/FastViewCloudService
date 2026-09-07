# -*- coding: utf-8 -*-
"""定位liberalism-lineage中未闭合的callout"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\liberalism-lineage\liberalism-lineage.html'
c = open(fp, encoding='utf-8').read()

# 找所有 callout 开标签位置，计算其后opens/closes差
for m in re.finditer(r'<div class="callout"', c):
    line = c[:m.start()].count('\n') + 1
    after = c[m.start():]
    opens = len(re.findall(r'<div[\s>]', after))
    closes = after.count('</div>')
    # 若该div是未闭合的，则其后 opens = closes + 1（含自身）
    tag = '未闭合' if opens == closes + 1 else ('正常' if opens <= closes else '异常')
    print('callout @行{}: 其后 opens={} closes={} diff={} [{}]'.format(line, opens, closes, opens - closes, tag))
