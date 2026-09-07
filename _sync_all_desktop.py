# -*- coding: utf-8 -*-
"""全库卷页面同步到桌面版（英文目录 -> 中文目录链接转换）"""
import os, re, shutil, glob

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

en_to_cn = {
    'truth-dimensions': '真理的多维图景',
    'marxism-lineage': '马克思主义谱系',
    'economics-lineage': '经济思想谱系',
    'econ-part2-lineage': '经济思想谱系下篇',
    'psych-lineage': '心理学思想谱系',
    'math-lineage': '数学思想谱系',
    'logic-lineage': '逻辑与论证思想谱系',
    'philosophy-lineage': '西方哲学思想谱系',
    'science-lineage': '科学思想谱系',
    'social-thought': '社会思想谱系',
    'history-lineage': '历史思想谱系',
    'ethics-lineage': '伦理与道德思想谱系',
    'literature-lineage': '文学与语言思想谱系',
    'rhetoric-lineage': '修辞与演说思想谱系',
    'education-lineage': '教育思想谱系',
    'life-science-lineage': '生命科学思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系',
    'politics-lineage': '政治学通论',
    'liberalism-lineage': '自由主义谱系',
    'isms-glossary': '政治基础概念1',
    'law-lineage': '法哲学思想谱系',
    'eastern-thought-lineage': '东方思想谱系',
    'art-aesthetics-lineage': '艺术与美学思想谱系',
    'anthropology-lineage': '人类学思想谱系',
    'media-lineage': '传播与媒介思想谱系',
    'military-lineage': '军事与战略思想谱系',
    'ir-lineage': '国际关系思想谱系',
    'geo-lineage': '地理与环境思想谱系',
    'religion-lineage': '宗教学与神话',
    'astronomy-lineage': '天文学与宇宙学',
    'physics-lineage': '物理学',
    'chemistry-lineage': '化学',
    'cs-lineage': '计算机科学',
    'linguistics-lineage': '语言学',
    'medicine-lineage': '医学与健康',
}

# 1. 枚举工作区卷目录
vol_dirs = [d for d in os.listdir(ws)
            if os.path.isdir(os.path.join(ws, d))
            and not d.startswith('_') and not d.startswith('.')
            and d not in ('思想图谱系列', 'series-overview')]

print('=== 工作区卷目录 ({} 个) ==='.format(len(vol_dirs)))
for d in sorted(vol_dirs):
    print('  ', d)

# 2. 检查哪些在桌面版有对应中文目录
print()
print('=== 桌面映射检查 ===')
missing = []
for d in sorted(vol_dirs):
    cn = en_to_cn.get(d)
    if cn is None:
        missing.append(d)
        print('  !! {} 无映射'.format(d))
    elif not os.path.isdir(os.path.join(dt, cn)):
        missing.append(d)
        print('  !! {} -> {} 桌面目录不存在'.format(d, cn))
    else:
        print('  OK {} -> {}'.format(d, cn))
