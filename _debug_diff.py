# -*- coding: utf-8 -*-
"""排查 marxism div 标签差异 + 主题索引差异"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
desktop = r'c:\Users\Admin1\Desktop\Trae资料库'

# 1. marxism div 标签检查
print('=== marxism div 标签检查 ===')
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()
c_no_script = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL)

# 检查是否注释中包含 div
c_no_comment = re.sub(r'<!--.*?-->', '', c_no_script, flags=re.DOTALL)
d_opens = len(re.findall(r'<div\b', c_no_comment))
d_closes = len(re.findall(r'</div>', c_no_comment))
print(f'去掉script+注释后: div开={d_opens} 闭={d_closes} 差={d_opens-d_closes}')

# 检查style块
c_no_style = re.sub(r'<style.*?</style>', '', c_no_comment, flags=re.DOTALL)
d_opens2 = len(re.findall(r'<div\b', c_no_style))
d_closes2 = len(re.findall(r'</div>', c_no_style))
print(f'再去掉style后: div开={d_opens2} 闭={d_closes2} 差={d_opens2-d_closes2}')

# 检查是否有 <div /> 自闭合
self_close = len(re.findall(r'<div[^>]*/>', c_no_style))
print(f'自闭合div: {self_close}')

# 检查模板字符串中的 div
tmpl = len(re.findall(r'<div', re.sub(r'<style.*?</style>', '', c, flags=re.DOTALL)))
print(f'含style原始div开: {tmpl}')

# 逐行找可能的异常 - 找在script里被排除前的div
# 可能问题：某些div写在JS字符串里（如innerHTML拼接），排除script后丢失闭合
# 检查JS中的div
scripts = re.findall(r'<script.*?</script>', c, flags=re.DOTALL)
js_div_open = 0
js_div_close = 0
for s in scripts:
    js_div_open += len(re.findall(r'<div\b', s))
    js_div_close += len(re.findall(r'</div>', s))
print(f'JS中的div: 开={js_div_open} 闭={js_div_close}')

print()
print('=== 主题索引.html 差异 ===')
ws_fp = os.path.join(ws, '思想图谱系列', '主题索引.html')
dt_fp = os.path.join(desktop, '思想图谱系列', '主题索引.html')
wc = open(ws_fp, encoding='utf-8').read()
dc = open(dt_fp, encoding='utf-8').read()
print(f'工作区: {len(wc)} 字符, 桌面: {len(dc)} 字符, 差={len(dc)-len(wc)}')

# 找不同位置
import difflib
# 简化对比：检查链接映射是否都正确
ws_links = set(re.findall(r'href="\.\./([^"]*)"', wc))
dt_links = set(re.findall(r'href="\.\./([^"]*)"', dc))
ws_broken = [l for l in ws_links if not os.path.exists(os.path.normpath(os.path.join(ws, '思想图谱系列', '..', l)))]
dt_broken = [l for l in dt_links if not os.path.exists(os.path.normpath(os.path.join(desktop, '思想图谱系列', '..', l)))]
print(f'工作区断链: {len(ws_broken)}')
for b in sorted(ws_broken)[:5]:
    print(f'  {b}')
print(f'桌面断链: {len(dt_broken)}')
for b in sorted(dt_broken)[:5]:
    print(f'  {b}')

# 对比差异行
sm = difflib.SequenceMatcher(None, wc, dc)
diff_chars = sum(block.size for block in sm.get_opcodes() if block[0] != 'equal')
print(f'差异字符数: {diff_chars}')

# 找到第一个差异点
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print(f'\n第一个差异 {tag}: 工作区[{i1}:{i2}] 桌面[{j1}:{j2}]')
        print(f'  工作区: ...{wc[max(0,i1-40):i1]}【{wc[i1:i2]}】{wc[i2:i2+40]}...')
        print(f'  桌面:   ...{dc[max(0,j1-40):j1]}【{dc[j1:j2]}】{dc[j2:j2+40]}...')
        break