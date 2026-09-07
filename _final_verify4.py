# -*- coding: utf-8 -*-
"""规范化链接集合对比：确认工作区/桌面版目录页功能等价"""
import os, re

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# 桌面版中文目录 -> 工作区英文目录（完整映射）
cn_to_en = {
    '真理的多维图景': 'truth-dimensions', '马克思主义谱系': 'marxism-lineage',
    '经济思想谱系': 'economics-lineage', '经济思想谱系下篇': 'econ-part2-lineage',
    '心理学思想谱系': 'psych-lineage', '数学思想谱系': 'math-lineage',
    '逻辑与论证思想谱系': 'logic-lineage', '西方哲学思想谱系': 'philosophy-lineage',
    '科学思想谱系': 'science-lineage', '社会思想谱系': 'social-thought',
    '历史思想谱系': 'history-lineage', '伦理与道德思想谱系': 'ethics-lineage',
    '文学与语言思想谱系': 'literature-lineage', '修辞与演说思想谱系': 'rhetoric-lineage',
    '教育思想谱系': 'education-lineage', '生命科学思想谱系': 'life-science-lineage',
    '科技与人工智能思想谱系': 'tech-ai-lineage', '政治学通论': 'politics-lineage',
    '自由主义谱系': 'liberalism-lineage', '政治基础概念1': 'isms-glossary',
    '思想图谱系列': '思想图谱系列', 'series-overview': 'series-overview',
    '法哲学思想谱系': 'law-lineage', '东方思想谱系': 'eastern-thought-lineage',
    '艺术与美学思想谱系': 'art-aesthetics-lineage', '人类学思想谱系': 'anthropology-lineage',
    '传播与媒介思想谱系': 'media-lineage', '军事与战略思想谱系': 'military-lineage',
    '国际关系思想谱系': 'ir-lineage', '地理与环境思想谱系': 'geo-lineage',
    '宗教学与神话': 'religion-lineage', '天文学与宇宙学': 'astronomy-lineage',
    '物理学': 'physics-lineage', '化学': 'chemistry-lineage',
    '计算机科学': 'cs-lineage', '语言学': 'linguistics-lineage',
    '医学与健康': 'medicine-lineage',
}


def canon_links(c):
    """提取链接并规范化为 (目录, 文件名) 集合"""
    links = re.findall(r'href="\.\./([^"]*)"', c)
    out = set()
    for l in links:
        parts = l.split('/')
        if len(parts) < 2:
            continue
        d, f = parts[0], parts[-1]
        d = cn_to_en.get(d, d)  # 中文目录 -> 英文
        out.add((d, f))
    return out


for fname in ['index.html', '主题索引.html']:
    wc = open(os.path.join(ws, '思想图谱系列', fname), encoding='utf-8').read()
    dc = open(os.path.join(dt, '思想图谱系列', fname), encoding='utf-8').read()
    wl, dl = canon_links(wc), canon_links(dc)
    only_w = wl - dl
    only_d = dl - wl
    print('==== {} ===='.format(fname))
    print('  工作区链接集: {} 桌面版链接集: {}'.format(len(wl), len(dl)))
    if not only_w and not only_d:
        print('  [OK] 链接集合完全一致（功能等价）')
    else:
        for x in sorted(only_w):
            print('  仅工作区: {}/{}'.format(*x))
        for x in sorted(only_d):
            print('  仅桌面版: {}/{}'.format(*x))
    print()
