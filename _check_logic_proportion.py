# -*- coding: utf-8 -*-
"""检查 logic 卷的布局比例、CSS 冲突、可视化容器尺寸"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

print('=== 1. CSS 变量定义（各style块） ===')
styles = [(m.start(), m.group(1)) for m in re.finditer(r'<style[^>]*>([\s\S]*?)</style>', c, re.I)]
for bi, (pos, css) in enumerate(styles):
    line = c[:pos].count('\n') + 1
    root = re.search(r':root\s*\{([^}]*)\}', css)
    if root:
        print('  块%d @行%d: %s' % (bi+1, line, re.sub(r'\s+', ' ', root.group(1)).strip()[:160]))

print()
print('=== 2. 关键布局选择器冲突 ===')
selectors_to_check = ['body', r'\.shell', r'\.page', 'main', r'\.sec', r'\.masthead', 'footer', 'article']
for bi, (pos, css) in enumerate(styles):
    for sel in selectors_to_check:
        for m in re.finditer(sel + r'\s*\{[^}]*\}', css):
            print('  块%d: %s' % (bi+1, re.sub(r'\s+', ' ', m.group(0)).strip()[:200]))

print()
print('=== 3. 可视化容器尺寸 ===')
for cid in ['three-container', 'chart-complexity', 'chart-methodology', 'animation-logic-paths']:
    m = re.search(r'<[^>]+id="' + cid + r'"[^>]*>', c)
    if m:
        line = c[:m.start()].count('\n') + 1
        # 找style
        ist = re.search(r'style="([^"]*)"', m.group(0))
        st = ist.group(1) if ist else '(无内联style)'
        print('  #%s @行%d: %s' % (cid, line, st))
        # CSS定义
        for bi, (pos2, css) in enumerate(styles):
            cm = re.search(r'#' + re.escape(cid) + r'\s*\{([^}]*)\}', css)
            if cm:
                print('    块%d CSS: %s' % (bi+1, re.sub(r'\s+', ' ', cm.group(1)).strip()[:200]))

print()
print('=== 4. 各 section 篇幅比例 ===')
lines = c.split('\n')
total = len(lines)
secs = [(m.start(), re.search(r'id="([^"]+)"', m.group(0))) for m in re.finditer(r'<section class="sec"[^>]*>', c)]
prev_line = 0
prev_id = '卷首'
for pos, idm in secs:
    line = c[:pos].count('\n') + 1
    span = line - prev_line
    pct = span / total * 100
    bar = '#' * max(1, round(span / 8))
    print('  %-24s %4d行 %5.1f%% %s' % (prev_id, span, pct, bar))
    prev_line = line
    prev_id = idm.group(1) if idm else '(无id)'
# 尾部
span = total - prev_line
pct = span / total * 100
print('  %-24s %4d行 %5.1f%%  [尾部脚本]' % (prev_id, span, pct))

print()
print('=== 5. 各 section 在 main 中的占比 ===')
main_start = c.find('<main')
main_end = c.rfind('</main>')
main_lines = c[main_start:main_end].count('\n')
print('  main 总行数: %d (占全卷 %.1f%%)' % (main_lines, main_lines/total*100))
# 显示 main 内部各 section 占比
secs_in_main = []
for m in re.finditer(r'<section[^>]*>', c):
    if main_start < m.start() < main_end:
        secs_in_main.append(m.start())
for i, pos in enumerate(secs_in_main):
    idm = re.search(r'id="([^"]+)"', c[pos:pos+200])
    sid = idm.group(1) if idm else '(无id)'
    next_pos = secs_in_main[i+1] if i+1 < len(secs_in_main) else main_end
    span = c[pos:next_pos].count('\n')
    pct = span / main_lines * 100
    bar = '#' * max(1, round(pct / 2))
    print('  %-24s %4d行 %5.1f%% %s' % (sid, span, pct, bar))

print()
print('=== 6. 重叠/遮挡检测 ===')
# 检查是否有 position: absolute/fixed 可能导致重叠
for m in re.finditer(r'position\s*:\s*(absolute|fixed|sticky)', c):
    line = c[:m.start()].count('\n') + 1
    print('  @行%d: position:%s' % (line, m.group(1)))