# -*- coding: utf-8 -*-
"""查看 overview section 完整内容"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# section 1 = overview @ 15756, section 2 = marx @ 20081
sec = c[15756:20081]
print(f'overview section 长度: {len(sec)}')
print(sec[:4000])
print('\n...\n')
print(sec[4000:8000])