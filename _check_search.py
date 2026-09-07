# -*- coding: utf-8 -*-
"""检查 _search_index.json 是否含英文路径引用"""
import os, re, json

dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# 1. _search_index.json
fp = os.path.join(dt, '思想图谱系列', '_search_index.json')
c = open(fp, encoding='utf-8').read()
print('=== _search_index.json ===')
print('  大小: %d KB' % (len(c)//1024))
# 找英文目录名引用
en_dirs = ['logic-lineage', 'math-lineage', 'truth-dimensions', 'marxism-lineage',
           'economics-lineage', 'psych-lineage', 'philosophy-lineage', 'science-lineage',
           'liberalism-lineage', 'econ-part2-lineage', 'social-thought', 'series-overview']
for en in en_dirs:
    cnt = c.count(en)
    if cnt:
        print('  英文引用 %-25s : %d 处' % (en, cnt))

# 找 .html 文件引用
html_refs = re.findall(r'["\']([^"\']*\.html)["\']', c)
print('  .html 引用总数: %d' % len(html_refs))
en_html = [h for h in html_refs if re.search(r'[a-z]+-lineage\.html|truth-dimensions\.html|social-thought\.html|eastern-thought\.html|isms-.*\.html', h)]
print('  英文 .html 引用: %d' % len(en_html))
for h in sorted(set(en_html))[:15]:
    print('    -> %s' % h)

print()
print('=== 人物索引.html / 阅读指南.html 是否含英文引用 ===')
for f in ['人物索引.html', '阅读指南.html']:
    fp2 = os.path.join(dt, '思想图谱系列', f)
    c2 = open(fp2, encoding='utf-8').read()
    en_in = [en for en in en_dirs if en in c2]
    data_href = re.findall(r'(?:href|data-href|data-path|src)="([^"]*)"', c2)
    print('  %s: 英文目录引用 %d 个 %s' % (f, len(en_in), en_in[:5] if en_in else ''))
    print('      href/src引用数: %d' % len(data_href))