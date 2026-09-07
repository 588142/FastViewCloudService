# -*- coding: utf-8 -*-
import os, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# (workspace_dir, workspace_file, desktop_dir, desktop_english_file, desktop_chinese_file)
pairs = [
    ('truth-dimensions', 'truth-dimensions.html', '真理的多维图景', 'truth-dimensions.html', '真理的多维图景.html'),
    ('marxism-lineage', 'marxism-lineage.html', '马克思主义谱系', 'marxism-lineage.html', '马克思主义谱系.html'),
    ('economics-lineage', 'economics-lineage.html', '经济思想谱系', 'economics-lineage.html', '经济思想谱系.html'),
    ('econ-part2-lineage', 'econ-part2-lineage.html', '经济思想谱系下篇', 'econ-part2-lineage.html', '经济思想谱系下篇.html'),
    ('psych-lineage', 'psych-lineage.html', '心理学思想谱系', 'psych-lineage.html', '心理学思想谱系.html'),
    ('math-lineage', 'math-lineage.html', '数学思想谱系', 'math-lineage.html', '数学思想谱系.html'),
]

for wd, wf, dd, defn, dcn in pairs:
    src = os.path.join(ws, wd, wf)
    dst_en = os.path.join(dt, dd, defn)
    dst_cn = os.path.join(dt, dd, dcn)
    
    if not os.path.exists(src):
        print(f'!! 源文件不存在: {src}')
        continue
    
    # 同步英文名
    if os.path.exists(dst_en):
        bak_en = dst_en + '.bak2'
        if not os.path.exists(bak_en):
            shutil.copy2(dst_en, bak_en)
    shutil.copy2(src, dst_en)
    en_size = os.path.getsize(dst_en)
    
    # 同步中文名
    if os.path.exists(dst_cn):
        bak_cn = dst_cn + '.bak2'
        if not os.path.exists(bak_cn):
            shutil.copy2(dst_cn, bak_cn)
    shutil.copy2(src, dst_cn)
    cn_size = os.path.getsize(dst_cn)
    
    # 校验
    src_zh = len(open(src, encoding='utf-8').read())
    en_zh = len(open(dst_en, encoding='utf-8').read())
    cn_zh = len(open(dst_cn, encoding='utf-8').read())
    
    match = '✅' if src_zh == en_zh == cn_zh else '⚠️ 大小不一致'
    print(f'{dd:15s} 英文={en_size//1024:>4}KB 中文={cn_size//1024:>4}KB {match}')

print('\n桌面同步完成！')