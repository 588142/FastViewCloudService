# -*- coding: utf-8 -*-
"""查看工作区 index.html 的链接写法"""
import re

ws = r'c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列\index.html'
c = open(ws, encoding='utf-8').read()

print('=== 工作区 index.html 所有 href 链接样式 ===')
hrefs = re.findall(r'href="([^"]*)"', c)
print('  href 总数:', len(hrefs))
# 分类
from collections import Counter
kinds = Counter()
samples = {}
for h in hrefs:
    if h.startswith('#') or h == '':
        k = '锚点#'
    elif h.startswith('http'):
        k = 'http外链'
    elif h.startswith('../'):
        k = '../相对路径'
    elif '/' in h:
        k = '含斜杠'
    elif h.endswith('.html'):
        k = '纯.html文件名'
    else:
        k = '其他'
    kinds[k] += 1
    samples.setdefault(k, []).append(h)
for k, cnt in kinds.most_common():
    print('  %-14s %d 个' % (k, cnt))
    print('    例:', samples[k][:5])