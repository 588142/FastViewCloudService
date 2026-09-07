# -*- coding: utf-8 -*-
import re, os
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = [
    ('truth-dimensions', 'truth-dimensions.html'),
    ('marxism-lineage', 'marxism-lineage.html'),
    ('economics-lineage', 'economics-lineage.html'),
    ('econ-part2-lineage', 'econ-part2-lineage.html'),
    ('psych-lineage', 'psych-lineage.html'),
    ('math-lineage', 'math-lineage.html'),
]
for d, f in vols:
    fp = os.path.join(ws, d, f)
    c = open(fp, encoding='utf-8').read()
    # find last chapter TOC link
    toc_links = re.findall(r'<li><a href="#summary">[^<]*</a></li>', c)
    if not toc_links:
        toc_links = re.findall(r'<li><a href="#ch\d+">[^<]*</a></li>', c)
    last_link = toc_links[-1] if toc_links else 'N/A'
    meta = re.search(r'<p class="meta">[^<]*</p>', c)
    meta_str = meta.group(0) if meta else 'N/A'
    print(f'=== {d} ===')
    print(f'TOC锚点: {last_link}')
    print(f'meta行: {meta_str}')
    print()