# -*- coding: utf-8 -*-
import re
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

# marxism getCenterPoint 上下文
c = open(ws + r'\marxism-lineage\marxism-lineage.html', encoding='utf-8').read()
print('=== marxism getCenterPoint ===')
for m in re.finditer(r'getCenterPoint\(\)', c):
    idx = m.start()
    line = c[:idx].count('\n') + 1
    print(f'  @line {line}: {c[max(0,idx-60):idx+25].replace(chr(10)," ")}')

# marxism dataset.label 2处
print('\n=== marxism dataset.label ===')
for m in re.finditer(r'context\.dataset\.label', c):
    idx = m.start()
    line = c[:idx].count('\n') + 1
    print(f'  @line {line}: ...{c[max(0,idx-80):idx+30].replace(chr(10)," ")}')

# economics datasets.map
c2 = open(ws + r'\economics-lineage\economics-lineage.html', encoding='utf-8').read()
print('\n=== economics datasets.map ===')
for m in re.finditer(r'datasets:\s*methods\.map', c2):
    idx = m.start()
    line = c2[:idx].count('\n') + 1
    print(f'  @line {line}: ...{c2[max(0,idx-40):idx+400].replace(chr(10)," ")[:440]}')
