# -*- coding: utf-8 -*-
"""检查可视化容器尺寸与上下文"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

for cid in ['chart-complexity', 'chart-methodology', 'animation-logic-paths', 'three-container']:
    m = re.search(r'<[^>]+id="' + cid + r'"[^>]*>', c)
    if m:
        line = c[:m.start()].count('\n') + 1
        ctx = c[max(0, m.start()-100):m.end()+100]
        print('=== %s (@行%d) ===' % (cid, line))
        print(ctx)
        print()
        # CSS定义
        for bi, (pos2, css) in enumerate([(m2.start(), m2.group(1)) for m2 in re.finditer(r'<style[^>]*>([\s\S]*?)</style>', c, re.I)]):
            cm = re.search(r'#' + re.escape(cid) + r'\s*\{([^}]*)\}', css)
            if cm:
                print('  CSS(块%d): %s' % (bi+1, re.sub(r'\s+', ' ', cm.group(1)).strip()[:200]))

print()
print('=== canvas 元素 ===')
for m in re.finditer(r'<canvas[^>]*>', c):
    line = c[:m.start()].count('\n') + 1
    print('  @行%d: %s' % (line, m.group(0)[:150]))
    pre = c[:m.start()]
    sec = re.findall(r'<section[^>]*id="([^"]*)"', pre)
    print('    父section: %s' % (sec[-1] if sec else '无'))

print()
print('=== three-container 完整 section 上下文 ===')
m = re.search(r'<div[^>]*id="three-container"[^>]*>', c)
if m:
    start = m.start()
    pre = c[:start]
    sec = list(re.finditer(r'<section[^>]*>', pre))
    if sec:
        sec_start = sec[-1].start()
        sec_end = c.find('</section>', sec_start)
        if sec_end > start:
            block = c[sec_start:sec_end+10]
            print('Section开头:', block[:500])
            print('...')
            print('Section结尾:', block[-200:])