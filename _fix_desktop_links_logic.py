# -*- coding: utf-8 -*-
"""修复桌面版逻辑卷跨卷链接"""
import os, re

dt = r'c:\Users\Admin1\Desktop\Trae资料库'
fp = os.path.join(dt, '逻辑与论证思想谱系', '逻辑与论证思想谱系.html')

en_to_cn = {
    'education-lineage': '教育思想谱系',
    'literature-lineage': '文学与语言思想谱系',
    'philosophy-lineage': '西方哲学思想谱系',
    'math-lineage': '数学思想谱系',
    'truth-dimensions': '真理的多维图景',
    'psych-lineage': '心理学思想谱系',
    'science-lineage': '科学思想谱系',
    'social-thought': '社会思想谱系',
    'eastern-thought-lineage': '东方思想谱系',
    'anthropology-lineage': '人类学思想谱系',
    'media-lineage': '传播与媒介思想谱系',
    'ethics-lineage': '伦理与道德思想谱系',
    'rhetoric-lineage': '修辞与演说思想谱系',
    'military-lineage': '军事与战略思想谱系',
    'history-lineage': '历史思想谱系',
    'ir-lineage': '国际关系思想谱系',
    'geo-lineage': '地理与环境思想谱系',
    'politics-lineage': '政治学通论',
    'law-lineage': '法哲学思想谱系',
    'life-science-lineage': '生命科学思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系',
    'economics-lineage': '经济思想谱系',
    'econ-part2-lineage': '经济思想谱系下篇',
    'liberalism-lineage': '自由主义谱系',
    'art-aesthetics-lineage': '艺术与美学思想谱系',
    'marxism-lineage': '马克思主义谱系',
    'logic-lineage': '逻辑与论证思想谱系',
    'science-lineage': '科学思想谱系',
    'social-thought': '社会思想谱系',
}

# 中文文件名映射
en_file_to_cn = {
    'education-lineage.html': '教育思想谱系.html',
    'literature-lineage.html': '文学与语言思想谱系.html',
    'philosophy-lineage.html': '西方哲学思想谱系.html',
    'math-lineage.html': '数学思想谱系.html',
    'truth-dimensions.html': '真理的多维图景.html',
    'psych-lineage.html': '心理学思想谱系.html',
    'science-lineage.html': '科学思想谱系.html',
    'social-thought.html': '社会思想谱系.html',
    'eastern-thought-lineage.html': '东方思想谱系.html',
    'anthropology-lineage.html': '人类学思想谱系.html',
    'media-lineage.html': '传播与媒介思想谱系.html',
    'ethics-lineage.html': '伦理与道德思想谱系.html',
    'rhetoric-lineage.html': '修辞与演说思想谱系.html',
    'military-lineage.html': '军事与战略思想谱系.html',
    'history-lineage.html': '历史思想谱系.html',
    'ir-lineage.html': '国际关系思想谱系.html',
    'geo-lineage.html': '地理与环境思想谱系.html',
    'politics-lineage.html': '政治学通论.html',
    'law-lineage.html': '法哲学思想谱系.html',
    'life-science-lineage.html': '生命科学思想谱系.html',
    'tech-ai-lineage.html': '科技与人工智能思想谱系.html',
    'economics-lineage.html': '经济思想谱系.html',
    'econ-part2-lineage.html': '经济思想谱系下篇.html',
    'liberalism-lineage.html': '自由主义谱系.html',
    'art-aesthetics-lineage.html': '艺术与美学思想谱系.html',
    'marxism-lineage.html': '马克思主义谱系.html',
    'logic-lineage.html': '逻辑与论证思想谱系.html',
    'science-lineage.html': '科学思想谱系.html',
    'social-thought.html': '社会思想谱系.html',
}

c = open(fp, encoding='utf-8').read()
old = c
# 第一步：转换目录名（../英文/ → ../中文/）
for en, cn in en_to_cn.items():
    c = c.replace('../' + en + '/', '../' + cn + '/')
# 第二步：转换文件名（../中文/英文.html → ../中文/中文.html）
for en_f, cn_f in en_file_to_cn.items():
    c = c.replace('/' + en_f, '/' + cn_f)

if c != old:
    open(fp, 'w', encoding='utf-8').write(c)
    print('链接已修复: %d处' % sum(c.count('../' + cn + '/') for cn in set(en_to_cn.values())))

# 验证
links = re.findall(r'href="([^"#]+?\.html)"', c)
base = os.path.dirname(fp)
broken = [l for l in links if not l.startswith('http') and not os.path.exists(os.path.normpath(os.path.join(base, l)))]
print('剩余断链: %d' % len(broken))
for b in broken[:5]:
    print('  ', b)