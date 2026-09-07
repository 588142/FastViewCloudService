# -*- coding: utf-8 -*-
"""检查 table-wrap CSS、TOC 条目、附录结构一致性"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

print('=== 1. table-wrap CSS 定义 ===')
for m in re.finditer(r'\.table-wrap\s*\{[^}]+\}', c):
    line = c[:m.start()].count('\n') + 1
    print('  @行{}: {}'.format(line, m.group(0).replace('\n', ' ')[:200]))

print()
print('=== 2. TOC 条目 ===')
mt = re.search(r'<ul class="toc"[^>]*>([\s\S]*?)</ul>', c)
if mt:
    items = re.findall(r'<a href="#([^"]+)"[^>]*>(.*?)</a>', mt.group(1), re.S)
    for i, t in items:
        print('   #{:<20s} {}'.format(i, re.sub(r'<[^>]+>', '', t).strip()[:45]))

print()
print('=== 3. 各 section 的行数（篇幅比例） ===')
secs = [(m.start(), re.search(r'id="([^"]+)"', m.group(0))) for m in re.finditer(r'<section class="sec"[^>]*>', c)]
lines = c.split('\n')
total = len(lines)
prev_line = None
prev_id = None
for pos, idm in secs:
    line = c[:pos].count('\n') + 1
    sid = idm.group(1) if idm else '(无id)'
    if prev_id is not None:
        span = line - prev_line
        bar = '#' * max(1, span // 6)
        print('  {:<22s} {:>4d}行 {}'.format(prev_id, span, bar))
    prev_line = line
    prev_id = sid
if prev_id:
    span = total - prev_line
    print('  {:<22s} {:>4d}行 {}'.format(prev_id, span, '#' * max(1, span // 6)))
print('  总行数:', total)

print()
print('=== 4. 附录/硕士模块内部结构一致性（h3数量） ===')
for pos, idm in secs:
    sid = idm.group(1) if idm else '(无id)'
    if not (sid.startswith('appendix') or sid.startswith('masters')):
        continue
    # 找该section到下一个section之间的内容
    next_pos = c.find('<section', pos + 10)
    end = next_pos if next_pos > 0 else len(c)
    block = c[pos:end]
    h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', block, re.S)
    line = c[:pos].count('\n') + 1
    print('  {:<22s} h3x{}: {}'.format(sid, len(h3s), ' | '.join(re.sub(r'<[^>]+>','',h).strip()[:18] for h in h3s[:5])))
