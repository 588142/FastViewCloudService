# -*- coding: utf-8 -*-
"""排查 logic-lineage 新增内容的结构/比例问题"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()
lines = c.split('\n')

print('=== 1. 所有 section 及其位置（是否在 <main> 内） ===')
main_open = c.find('<main')
main_close = c.rfind('</main>')
for m in re.finditer(r'<section[^>]*>', c):
    line = c[:m.start()].count('\n') + 1
    in_main = 'main内' if main_open < m.start() < main_close else '!!main外!!'
    print('  行{:>4d} {}  {}'.format(line, m.group(0)[:70], in_main))
print('  <main> @行{}  </main> @行{}'.format(c[:main_open].count('\n')+1 if main_open>=0 else -1, c[:main_close].count('\n')+1))

print()
print('=== 2. h2 标题清单（顺序） ===')
for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', c, re.S):
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:50]
    line = c[:m.start()].count('\n') + 1
    print('  行{:>4d} {}'.format(line, t))

print()
print('=== 3. TOC 链接 vs 实际锚点 ===')
toc_ids = re.findall(r'<a href="#([^"]+)"', c)
sec_ids = re.findall(r'<section[^>]*id="([^"]+)"', c)
missing = [t for t in set(toc_ids) if t not in sec_ids and t not in re.findall(r'id="([^"]+)"', c)]
print('  TOC锚点数:', len(toc_ids), ' 断锚:', missing if missing else '无')

print()
print('=== 4. 可视化容器尺寸（内联style的height/width） ===')
for m in re.finditer(r'<(div|canvas|figure)[^>]*style="([^"]*)"[^>]*>', c):
    st = m.group(2)
    if 'height' in st or 'width' in st:
        line = c[:m.start()].count('\n') + 1
        print('  行{:>4d} <{}> {}'.format(line, m.group(1), st[:100]))

print()
print('=== 5. CSS 中的高度类定义 ===')
for m in re.finditer(r'\.([\w-]+)\s*\{[^}]*height\s*:\s*([^;]+);', c):
    print('  .{}  height:{}'.format(m.group(1), m.group(2).strip()))
