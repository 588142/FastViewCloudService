# -*- coding: utf-8 -*-
import re
c = open(r'c:\Users\Admin1\Documents\FastViewCloudService\psych-lineage\psych-lineage.html', encoding='utf-8').read()
for m in re.finditer(r'afterDraw', c):
    idx = m.start()
    line = c[:idx].count('\n') + 1
    seg = c[max(0, idx-200):idx+700]
    print(f'afterDraw @line {line}:')
    print(seg.replace('\n', ' ⏎ ')[:800])
    print()
