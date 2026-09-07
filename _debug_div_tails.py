# -*- coding: utf-8 -*-
"""查看7个未闭合div的完整内容区间（开标签到最近的</section>），确定补闭合位置"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

targets = [
    ('<div class="callout"><figure class="diagram">', 'line440'),
    ('<div class="callout"><span class="callout-title">一条主线</span>', 'line478'),
    ('<div class="table-wrap">        <div class="table-wrap">', 'line553'),
    ('<div class="table-wrap">        <div class="table-wrap">', 'line714'),
    ('<div class="table-wrap">        <div class="table-wrap">', 'line1015'),
    ('<div class="table-wrap">        <div class="table-wrap">', 'line1093'),
    ('<div class="callout">        <div class="callout">', 'line1148'),
]

for pat, name in targets:
    idx = c.find(pat)
    if idx == -1:
        print(f'== {name}: 未找到 [{pat[:40]}]')
        continue
    line = c[:idx].count('\n') + 1
    # 找该div后第一个 </section>
    sec_close = c.find('</section>', idx)
    seg = c[idx:sec_close] if sec_close != -1 else c[idx:idx+2000]
    print(f'== {name} @ line {line} | 长度{len(seg)} | 到</section>@line {c[:sec_close].count(chr(10))+1}')
    # 显示该段的最后300字符（闭合前）
    tail = seg[-300:].replace('\n', ' ⏎ ')
    print(f'   末尾: ...{tail}')
    print()
