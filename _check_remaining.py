# -*- coding: utf-8 -*-
"""检查剩余问题：重复id、断锚、CSS块大小"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

styles = [(m.start(), m.group(1)) for m in re.finditer(r'<style[^>]*>([\s\S]*?)</style>', c, re.I)]
for bi, (pos, css) in enumerate(styles):
    line = c[:pos].count('\n') + 1
    print('CSS块%d @行%d: %d 字符' % (bi+1, line, len(css)))

# 重复id
ids = {}
for m in re.finditer(r'id="([^"]+)"', c):
    iid = m.group(1)
    ids.setdefault(iid, []).append(c[:m.start()].count('\n') + 1)
dupes = {k: v for k, v in ids.items() if len(v) > 1}
print('\n重复id: %d个' % len(dupes))
for k, v in sorted(dupes.items()):
    print('  id="%s" @行 %s' % (k, v))

# TOC断锚
toc_ids = re.findall(r'href="#([^"]+)"', c[:2000])
html_ids = set(re.findall(r'id="([^"]+)"', c))
missing = [t for t in toc_ids if t not in html_ids]
print('\nTOC断锚: %d个' % len(missing))
if missing:
    print('  ', missing[:10])