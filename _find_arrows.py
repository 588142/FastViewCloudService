# -*- coding: utf-8 -*-
import re
c = open(r'c:\Users\Admin1\Documents\FastViewCloudService\marxism-lineage\marxism-lineage.html', encoding='utf-8').read()
for m in re.finditer(r'arrows\s*=', c):
    idx = m.start()
    line = c[:idx].count('\n') + 1
    seg = c[idx:idx+300].replace('\n', ' ')
    print(f'arrows定义 @line {line}:')
    print(f'  {seg[:300]}')
    print()
