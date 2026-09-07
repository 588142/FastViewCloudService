# -*- coding: utf-8 -*-
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
for d in ['truth-dimensions','economics-lineage']:
    fp = os.path.join(ws, d, d + '.html')
    c = open(fp, encoding='utf-8').read()
    links = re.findall(r'<li><a href="#[^"]*">[^<]*</a></li>', c)
    print(f'=== {d} ({len(links)} TOC links) ===')
    for l in links[-3:]:
        print('  ', l)
    print(f'  has #summary: {"#summary" in c}')
    # also check for any #ch links
    ch_links = re.findall(r'<li><a href="#ch\d+">[^<]*</a></li>', c)
    print(f'  chapter links: {len(ch_links)}')
    for l in ch_links[-2:]:
        print('  ', l)
    print()