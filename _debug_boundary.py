# -*- coding: utf-8 -*-
"""确认重复块边界 + 文件末尾结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 1. 各section中 图1a 和 explain 的出现
print('=== 各section中"图 1a"出现情况 ===')
sections = [(m.start(), m.group(0)) for m in re.finditer(r'<section[^>]*>', c)]
for idx in [1, 3, 5, 6]:
    sec_start = sections[idx][0]
    sec_end = sections[idx+1][0] if idx+1 < len(sections) else len(c)
    sec = c[sec_start:sec_end]
    fig1a = sec.count('图 1a')
    explain = sec.count('class="explain"')
    table_wrap = sec.count('class="table-wrap"')
    print(f'  section {idx} ({sections[idx][1][:40]}): 图1a={fig1a}, explain={explain}, table-wrap开={table_wrap}')

# 2. lenin section 的完整内容
print('\n=== lenin section (22447-28272) 前3000字符 ===')
print(c[22447:22447+3000])

# 3. 文件末尾结构
print('\n=== 文件末尾 3000 字符 ===')
print(c[-3000:])