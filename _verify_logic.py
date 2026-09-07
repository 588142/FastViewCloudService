# -*- coding: utf-8 -*-
"""修复后全量校验 logic-lineage"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

print('=== 1. 基本框架 ===')
for tag, name in [('<!DOCTYPE', 'DOCTYPE'), ('<html', 'html开'), ('</html>', 'html闭'),
                  ('<head>', 'head开'), ('</head>', 'head闭'), ('<body', 'body开'), ('</body>', 'body闭'),
                  ('class="shell"', 'shell容器'), ('<footer', 'footer')]:
    print('  {}: {}'.format(name, c.count(tag)))

c2 = re.sub(r'<script[\s\S]*?</script>', '', c, flags=re.I)
c2 = re.sub(r'<style[\s\S]*?</style>', '', c2, flags=re.I)
print()
print('=== 2. 标签平衡（剥离脚本后） ===')
for tag in ['div', 'section', 'table', 'figure', 'ul', 'main', 'article']:
    o = len(re.findall(r'<' + tag + r'[\s>]', c2))
    cl = c2.count('</' + tag + '>')
    print('  {}: {} / {} {}'.format(tag, o, cl, 'OK' if o == cl else '!!'))

print()
print('=== 3. 所有 section 均在 <main> 内 ===')
mo = c.find('<main')
mc = c.rfind('</main>')
bad = 0
for m in re.finditer(r'<section[^>]*>', c):
    if not (mo < m.start() < mc):
        print('  !! main外 section @行{}'.format(c[:m.start()].count('\n') + 1))
        bad += 1
print('  main外section数:', bad)

print()
print('=== 4. 锚点 ===')
ids = set(re.findall(r'id="([^"]+)"', c))
anchors = re.findall(r'href="#([^"]+)"', c)
broken = [a for a in anchors if a not in ids]
print('  锚点{}个, 断锚{}个'.format(len(anchors), len(broken)), broken if broken else '')

print()
print('=== 5. 链接 ===')
import os
base = os.path.dirname(fp)
links = re.findall(r'href="([^"#]+?\.html)"', c)
broken_l = []
for l in links:
    if l.startswith(('http', 'mailto')):
        continue
    if not os.path.exists(os.path.normpath(os.path.join(base, l))):
        broken_l.append(l)
print('  链接{}个, 断链{}个'.format(len(links), len(broken_l)), broken_l if broken_l else '')

print()
print('=== 6. footer 与正文一致性 ===')
print('  footer数:', c.count('<footer'))
for m in re.finditer(r'<footer[^>]*>([\s\S]*?)</footer>', c):
    print('  内容:', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip()[:80])
