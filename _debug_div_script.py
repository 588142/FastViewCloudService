# -*- coding: utf-8 -*-
"""验证：未闭合div是否在script/字符串内部"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 找出所有script块的真实边界
script_bounds = []
for m in re.finditer(r'<script', c):
    end = c.find('</script>', m.end())
    if end == -1:
        print(f'⚠️ 未闭合script @ {m.start()}')
        continue
    script_bounds.append((m.start(), end + len('</script>')))
print(f'script块: {len(script_bounds)} 个')

# 找出所有div开标签，检查是否在script块内
divs = list(re.finditer(r'<div(?:\s[^>]*)?>', c))
in_script = []
out_script = []
for m in divs:
    pos = m.start()
    inside = any(s <= pos < e for s, e in script_bounds)
    (in_script if inside else out_script).append(m)

print(f'div总数: {len(divs)}, 在script内: {len(in_script)}, 在HTML内: {len(out_script)}')
print(f'\n在script内的div标签:')
for m in in_script:
    line = c[:m.start()].count('\n') + 1
    print(f'  line {line}: {c[m.start():m.start()+70].splitlines()[0][:70]}')

# 检查script内部是否有 '  </div>' 字符串
print(f'\nscript内 </div> 字符串:')
div_close_in_script = 0
for s, e in script_bounds:
    seg = c[s:e]
    n = len(re.findall(r'</div>', seg))
    if n:
        div_close_in_script += n
print(f'  script内的</div>: {div_close_in_script}')
