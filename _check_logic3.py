# -*- coding: utf-8 -*-
"""检查 logic 卷可视化容器位置/尺寸 + footer/masthead 重复"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

print('=== 1. footer 出现次数与内容 ===')
for m in re.finditer(r'<footer[^>]*>([\s\S]*?)</footer>', c):
    line = c[:m.start()].count('\n') + 1
    txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:70]
    print('  @行{}: {}'.format(line, txt))

print()
print('=== 2. masthead / series-bar 出现次数 ===')
print('  masthead:', len(re.findall(r'class="masthead"', c)))
print('  series-bar:', len(re.findall(r'class="series-bar"', c)))
print('  sidenav:', len(re.findall(r'class="sidenav"', c)))
print('  toc ul:', len(re.findall(r'class="toc"', c)))

print()
print('=== 3. 可视化容器（id 被 JS 引用） ===')
# JS中 getElementById 引用的 id
js_ids = re.findall(r'getElementById\([\'"]([^\'"]+)[\'"]\)', c)
print('  JS引用的id:', js_ids)
for jid in set(js_ids):
    # 找对应元素
    m = re.search(r'<(\w+)[^>]*id="' + re.escape(jid) + r'"[^>]*>', c)
    if m:
        line = c[:m.start()].count('\n') + 1
        print('  [{}] @行{}: {}'.format(jid, line, m.group(0)[:130]))
    else:
        print('  [{}] !! 元素不存在'.format(jid))

print()
print('=== 4. 容器尺寸相关 CSS 类 ===')
for cls in ['three-container', 'chart', 'canvas-wrap', 'viz', 'diagram']:
    for m in re.finditer(r'\.' + re.escape(cls) + r'[^{]*\{([^}]*)\}', c):
        line = c[:m.start()].count('\n') + 1
        print('  @行{} .{} {{ {} }}'.format(line, cls, m.group(1).strip()[:120]))

print()
print('=== 5. canvas 元素 ===')
for m in re.finditer(r'<canvas[^>]*>', c):
    line = c[:m.start()].count('\n') + 1
    print('  @行{}: {}'.format(line, m.group(0)[:130]))

print()
print('=== 6. masters 模块的 figure/table-wrap 数量 ===')
ms = c.find('id="masters-prologue"')
if ms > 0:
    tail = c[ms:]
    print('  masters区 figure:', len(re.findall(r'<figure', tail)))
    print('  masters区 table:', len(re.findall(r'<table', tail)))
    print('  masters区 canvas:', len(re.findall(r'<canvas', tail)))
    print('  masters区 div[id]:', re.findall(r'<div id="([^"]+)"', tail))
