# -*- coding: utf-8 -*-
import os, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

pairs = [
    ('truth-dimensions', 'truth-dimensions.html', '真理的多维图景', 'truth-dimensions.html', '真理的多维图景.html'),
    ('marxism-lineage', 'marxism-lineage.html', '马克思主义谱系', 'marxism-lineage.html', '马克思主义谱系.html'),
    ('economics-lineage', 'economics-lineage.html', '经济思想谱系', 'economics-lineage.html', '经济思想谱系.html'),
    ('econ-part2-lineage', 'econ-part2-lineage.html', '经济思想谱系下篇', 'econ-part2-lineage.html', '经济思想谱系下篇.html'),
    ('psych-lineage', 'psych-lineage.html', '心理学思想谱系', 'psych-lineage.html', '心理学思想谱系.html'),
    ('math-lineage', 'math-lineage.html', '数学思想谱系', 'math-lineage.html', '数学思想谱系.html'),
    ('logic-lineage', 'logic-lineage.html', '逻辑与论证思想谱系', 'logic-lineage.html', '逻辑与论证思想谱系.html'),
]

for wd, wf, dd, defn, dcn in pairs:
    src = os.path.join(ws, wd, wf)
    for dst_name in [defn, dcn]:
        dst = os.path.join(dt, dd, dst_name)
        if os.path.exists(dst):
            bak = dst + '.bak3'
            if not os.path.exists(bak):
                shutil.copy2(dst, bak)
        shutil.copy2(src, dst)
    
    en_size = os.path.getsize(os.path.join(dt, dd, defn))
    cn_size = os.path.getsize(os.path.join(dt, dd, dcn))
    ok = '✅' if en_size == cn_size else '⚠️'
    print(f'{dd:15s} 英文={en_size//1024:>3}KB 中文={cn_size//1024:>3}KB {ok}')

print('\n桌面同步完成！')