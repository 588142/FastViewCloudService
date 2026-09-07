# -*- coding: utf-8 -*-
"""精确同步验证：归一化链接路径后对比内容"""
import os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# 桌面版：中文目录 -> 工作区英文目录
cn_to_en = {
    '真理的多维图景': 'truth-dimensions',
    '马克思主义谱系': 'marxism-lineage',
    '经济思想谱系': 'economics-lineage',
    '经济思想谱系下篇': 'econ-part2-lineage',
    '心理学思想谱系': 'psych-lineage',
    '数学思想谱系': 'math-lineage',
    '逻辑与论证思想谱系': 'logic-lineage',
    '西方哲学思想谱系': 'philosophy-lineage',
    '科学思想谱系': 'science-lineage',
    '社会思想谱系': 'social-thought',
    '历史思想谱系': 'history-lineage',
    '伦理与道德思想谱系': 'ethics-lineage',
    '文学与语言思想谱系': 'literature-lineage',
    '修辞与演说思想谱系': 'rhetoric-lineage',
    '教育思想谱系': 'education-lineage',
    '生命科学思想谱系': 'life-science-lineage',
    '科技与人工智能思想谱系': 'tech-ai-lineage',
    '政治学通论': 'politics-lineage',
    '自由主义谱系': 'liberalism-lineage',
    '政治基础概念1': 'isms-glossary',
    '思想图谱系列': '思想图谱系列',
    'series-overview': 'series-overview',
}


def normalize(c):
    """把桌面版内容中的中文目录路径还原为英文，再比较"""
    for cn, en in cn_to_en.items():
        c = c.replace('../' + cn + '/', '../' + en + '/')
    return c


print('=== 1. 标星卷内容一致性（归一化链接后） ===')
star_vols = [
    ('truth-dimensions', '真理的多维图景'),
    ('marxism-lineage', '马克思主义谱系'),
    ('economics-lineage', '经济思想谱系'),
    ('econ-part2-lineage', '经济思想谱系下篇'),
    ('psych-lineage', '心理学思想谱系'),
    ('math-lineage', '数学思想谱系'),
    ('logic-lineage', '逻辑与论证思想谱系'),
]
all_ok = True
for en, cn in star_vols:
    wf = os.path.join(ws, en, en + '.html')
    with open(wf, encoding='utf-8') as f:
        wc = f.read()
    for fname in [en + '.html', cn + '.html']:
        df = os.path.join(dt, cn, fname)
        if not os.path.exists(df):
            print('  !! {}: {} 缺失'.format(cn, fname))
            all_ok = False
            continue
        with open(df, encoding='utf-8') as f:
            dc = normalize(f.read())
        if dc == wc:
            print('  [OK] {:<20s} {}'.format(cn, fname))
        else:
            all_ok = False
            # 找出差异位置
            i = 0
            while i < min(len(wc), len(dc)) and wc[i] == dc[i]:
                i += 1
            print('  [DIFF] {:<20s} {}  首个差异@{}'.format(cn, fname, i))
            print('        工作区: ...{}...'.format(wc[max(0, i-60):i+60].replace(chr(10), ' ')))
            print('        桌面版: ...{}...'.format(dc[max(0, i-60):i+60].replace(chr(10), ' ')))

print()
print('=== 2. 目录页/阅读指南一致性 ===')
for fname in ['index.html', '阅读指南.html', '主题索引.html']:
    wf = os.path.join(ws, '思想图谱系列', fname)
    df = os.path.join(dt, '思想图谱系列', fname)
    if not (os.path.exists(wf) and os.path.exists(df)):
        print('  !! {} 缺失 (ws={} dt={})'.format(fname, os.path.exists(wf), os.path.exists(df)))
        all_ok = False
        continue
    with open(wf, encoding='utf-8') as f:
        wc = f.read()
    with open(df, encoding='utf-8') as f:
        dc = normalize(f.read())
    if dc == wc:
        print('  [OK] {}'.format(fname))
    else:
        all_ok = False
        i = 0
        while i < min(len(wc), len(dc)) and wc[i] == dc[i]:
            i += 1
        print('  [DIFF] {} 首个差异@{}'.format(fname, i))
        print('        工作区: ...{}...'.format(wc[max(0, i-60):i+60].replace(chr(10), ' ')))
        print('        桌面版: ...{}...'.format(dc[max(0, i-60):i+60].replace(chr(10), ' ')))

print()
print('结论:', '全部一致，同步完成' if all_ok else '存在差异，需处理')
