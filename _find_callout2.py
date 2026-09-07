# -*- coding: utf-8 -*-
"""宽松匹配所有callout标签"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\liberalism-lineage\liberalism-lineage.html'
c = open(fp, encoding='utf-8').read()

# 所有 class 含 callout 的 div
for m in re.finditer(r'<div[^>]*class=["\'][^"\']*callout[^"\']*["\'][^>]*>', c):
    line = c[:m.start()].count('\n') + 1
    after = c[m.start():]
    opens = len(re.findall(r'<div[\s>]', after))
    closes = after.count('</div>')
    tag = '未闭合!' if opens == closes + 1 else 'OK'
    print('callout @行{}: opens={} closes={} diff={} [{}]'.format(line, opens, closes, opens - closes, tag))

print()
# 所有 div 开标签与其class（前90个）
for i, m in enumerate(re.finditer(r'<div[^>]*>', c)):
    line = c[:m.start()].count('\n') + 1
    t = m.group(0)
    if 'callout' in t or 'table-wrap' in t or 'explain' in t:
        print('行{}: {}'.format(line, t[:80]))
