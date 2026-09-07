# -*- coding: utf-8 -*-
"""检查masters区容器类定义"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

for cls in ['viz-container', 'chart-wrapper', 'animation-wrapper', 'three-container',
            'chart-complexity', 'chart-methodology', 'animation-logic-paths']:
    found = list(re.finditer(r'\.' + re.escape(cls) + r'\s*\{([^}]*)\}', c))
    if found:
        for m in found:
            line = c[:m.start()].count('\n') + 1
            print('@行{} .{} {{ {} }}'.format(line, cls, re.sub(r'\s+', ' ', m.group(1)).strip()[:150]))
    else:
        # 检查是否有 #id 定义
        found2 = list(re.finditer(r'#' + re.escape(cls) + r'\s*\{([^}]*)\}', c))
        if found2:
            for m in found2:
                line = c[:m.start()].count('\n') + 1
                print('@行{} #{} {{ {} }}'.format(line, cls, re.sub(r'\s+', ' ', m.group(1)).strip()[:150]))
        else:
            print('.{} 无CSS定义'.format(cls))
