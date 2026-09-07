# -*- coding: utf-8 -*-
import os, shutil
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'
pairs = [
    ('truth-dimensions', '真理的多维图景', 'truth-dimensions.html', '真理的多维图景.html'),
    ('marxism-lineage', '马克思主义谱系', 'marxism-lineage.html', '马克思主义谱系.html'),
    ('economics-lineage', '经济思想谱系', 'economics-lineage.html', '经济思想谱系.html'),
    ('econ-part2-lineage', '经济思想谱系下篇', 'econ-part2-lineage.html', '经济思想谱系下篇.html'),
    ('psych-lineage', '心理学思想谱系', 'psych-lineage.html', '心理学思想谱系.html'),
    ('math-lineage', '数学思想谱系', 'math-lineage.html', '数学思想谱系.html'),
]
for wd, dd, en, cn in pairs:
    src = os.path.join(ws, wd, wd + '.html')
    for fn in [en, cn]:
        dst = os.path.join(dt, dd, fn)
        shutil.copy2(src, dst)
    es = os.path.getsize(os.path.join(dt, dd, en)) // 1024
    cs = os.path.getsize(os.path.join(dt, dd, cn)) // 1024
    print(f'{dd:15s} 英文={es:>3}KB 中文={cs:>3}KB')
print('桌面同步完成！')