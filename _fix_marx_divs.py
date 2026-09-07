# -*- coding: utf-8 -*-
"""修复marxism-lineage的8处未闭合div
1. [2]+[3]: explain后补</div> + 删重复"一条主线"外层callout
2. [4][5][6][7]: 删4处双table-wrap的外层开标签
3. [8]+line1195: 删2处双callout的外层开标签
"""
import re, os, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

orig_div_open = len(re.findall(r'<div(?:\s[^>]*)?>', c))
orig_div_close = len(re.findall(r'</div>', c))
print(f'修复前: <div>={orig_div_open} </div>={orig_div_close} 差={orig_div_open-orig_div_close}')

# === 1. [2]+[3] 合并块 ===
p3 = ('        </div>\n'
      '        <div class="callout">\n'
      '          <span class="callout-title">一条主线</span>        <div class="callout">\n'
      '          <span class="callout-title">一条主线</span>')
r3 = ('        </div>\n'
      '        </div>\n'
      '        <div class="callout">\n'
      '          <span class="callout-title">一条主线</span>')
n3 = c.count(p3)
print(f'[2]+[3] 一条主线块: {n3} 处')
if n3 == 1:
    c = c.replace(p3, r3, 1)
else:
    print(f'  ⚠️ 数量异常，跳过')

# === 2. 双table-wrap：删外层开 ===
p1 = '<div class="table-wrap">        <div class="table-wrap">'
r1 = '<div class="table-wrap">'
n1 = c.count(p1)
print(f'双table-wrap: {n1} 处')
c = c.replace(p1, r1)

# === 3. 双callout：删外层开 ===
p2 = '<div class="callout">        <div class="callout">'
r2 = '<div class="callout">'
n2 = c.count(p2)
print(f'双callout: {n2} 处')
c = c.replace(p2, r2)

# === 验证 ===
new_div_open = len(re.findall(r'<div(?:\s[^>]*)?>', c))
new_div_close = len(re.findall(r'</div>', c))
print(f'修复后: <div>={new_div_open} </div>={new_div_close} 差={new_div_open-new_div_close}')

ok = (new_div_open == new_div_close and n3 == 1 and n1 == 4 and n2 == 2)
if ok:
    bak = fp + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    open(fp, 'w', encoding='utf-8').write(c)
    print('✅ 修复完成并写回')
else:
    print('⚠️ 验证未通过，未写回')
