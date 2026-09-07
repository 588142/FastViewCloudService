# -*- coding: utf-8 -*-
"""检查可视化容器父级结构与尺寸"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

for cid in ['three-container', 'chart-complexity', 'chart-methodology', 'animation-logic-paths']:
    m = re.search(r'<[^>]+id="' + cid + r'"[^>]*>', c)
    if m:
        line = c[:m.start()].count('\n') + 1
        ctx = c[max(0, m.start() - 300):m.start()]
        parents = re.findall(r'<(\w+)[^>]*class="([^"]+)"', ctx)
        print('{} @行{}'.format(cid, line))
        print('   元素: {}'.format(m.group(0)[:100]))
        print('   父级: {}'.format([p[1] for p in parents[-2:]]))
        print()

# .viz 与 .chart 定义
print('=== 容器样式 ===')
for m in re.finditer(r'\.(viz|chart|three-container)[^{]*\{([^}]*)\}', c):
    print('  .{}{{{}}}'.format(m.group(1), re.sub(r'\s+', ' ', m.group(2)).strip()[:130]))
