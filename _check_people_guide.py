# -*- coding: utf-8 -*-
"""查看人物索引/阅读指南的 href 内容 + 检查是否有指向卷的跳转"""
import os, re

dt = r'c:\Users\Admin1\Desktop\Trae资料库'

for f in ['人物索引.html', '阅读指南.html']:
    fp = os.path.join(dt, '思想图谱系列', f)
    c = open(fp, encoding='utf-8').read()
    hrefs = re.findall(r'(?:href|src|data-href)="([^"]*)"', c)
    print('=== %s (%d 个引用) ===' % (f, len(hrefs)))
    for h in sorted(set(hrefs))[:30]:
        print('  %s' % h)
    print()