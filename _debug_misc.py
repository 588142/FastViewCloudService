# -*- coding: utf-8 -*-
"""检查 marxism 悬空 section 和主内容结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 1. 悬空 section @99790
print('=== 悬空 section @99769-100469 ===')
print(c[99769:100469])

# 2. 主内容开头结构 @10445-11506
print('\n=== 主内容开头 @10445-11506 ===')
print(c[10445:11506])