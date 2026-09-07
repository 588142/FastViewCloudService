# -*- coding: utf-8 -*-
"""同步marxism-lineage到桌面版（chart bug修复后）"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

dir_map = {
    'econ-part2-lineage': '经济思想谱系下篇', 'economics-lineage': '经济思想谱系',
    'education-lineage': '教育思想谱系', 'ethics-lineage': '伦理与道德思想谱系',
    'history-lineage': '历史思想谱系', 'isms-glossary': '政治基础概念1',
    'liberalism-lineage': '自由主义谱系', 'life-science-lineage': '生命科学思想谱系',
    'literature-lineage': '文学与语言思想谱系', 'logic-lineage': '逻辑与论证思想谱系',
    'marxism-lineage': '马克思主义谱系', 'math-lineage': '数学思想谱系',
    'philosophy-lineage': '西方哲学思想谱系', 'politics-lineage': '政治学通论',
    'psych-lineage': '心理学思想谱系', 'rhetoric-lineage': '修辞与演说思想谱系',
    'science-lineage': '科学思想谱系', 'social-thought': '社会思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系', 'truth-dimensions': '真理的多维图景',
    'series-overview': 'series-overview', '思想图谱系列': '思想图谱系列',
}

src = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(src, encoding='utf-8').read()
for en, cn in dir_map.items():
    c = c.replace(f'../{en}/', f'../{cn}/')

dst_dir = os.path.join(dt, '马克思主义谱系')
for dst in [os.path.join(dst_dir, 'marxism-lineage.html'),
            os.path.join(dst_dir, '马克思主义谱系.html')]:
    open(dst, 'w', encoding='utf-8').write(c)

# 验证
problems = []
for cl in re.findall(r'href="\.\./([^"]*)"', c):
    if not os.path.exists(os.path.normpath(os.path.join(dst_dir, '..', cl))):
        problems.append(cl)
print('marxism 桌面同步:', '✅' if not problems else f'⚠️ 断链{problems}')
