# -*- coding: utf-8 -*-
"""用difflib精确对比 index.html / 主题索引.html 的真实差异"""
import os, difflib

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

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
    '艺术与美学思想谱系': 'art-aesthetics-lineage',
    '人类学思想谱系': 'anthropology-lineage', '传播与媒介思想谱系': 'media-lineage',
    '军事与战略思想谱系': 'strategy-lineage', '国际关系思想谱系': 'ir-lineage',
    '地理与环境思想谱系': 'geo-env-lineage', '宗教学与神话': 'religion-myth',
    '天文学与宇宙学': 'astronomy', '物理学': 'physics', '化学': 'chemistry',
    '计算机科学': 'computer-science', '语言学': 'linguistics',
    '医学与健康': 'medicine-health',
}


def normalize(c):
    for cn, en in cn_to_en.items():
        c = c.replace('../' + cn + '/', '../' + en + '/')
    return c


for fname in ['index.html', '主题索引.html']:
    wf = os.path.join(ws, '思想图谱系列', fname)
    df = os.path.join(dt, '思想图谱系列', fname)
    wc = open(wf, encoding='utf-8').read()
    dc = normalize(open(df, encoding='utf-8').read())
    if wc == dc:
        print('[OK] {} 完全一致'.format(fname))
        continue
    wl = wc.splitlines()
    dl = dc.splitlines()
    sm = difflib.SequenceMatcher(None, wl, dl)
    print()
    print('==== {} 差异明细 ===='.format(fname))
    count = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        count += 1
        if count > 15:
            print('  ... 还有更多差异')
            break
        if tag == 'replace':
            print('  [替换] 工作区行{}: {}'.format(i1, wl[i1][:150]))
            print('         桌面版行{}: {}'.format(j1, dl[j1][:150]))
        elif tag == 'delete':
            print('  [删除] 工作区行{}: {}'.format(i1, wl[i1][:150]))
        elif tag == 'insert':
            print('  [新增] 桌面版行{}: {}'.format(j1, dl[j1][:150]))
    print('  总差异块数: {}'.format(count))
