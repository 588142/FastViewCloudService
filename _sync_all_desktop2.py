# -*- coding: utf-8 -*-
"""全量同步：工作区所有卷页面 -> 桌面版（英文目录 -> 中文目录链接转换）"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

en_to_cn = {
    'truth-dimensions': '真理的多维图景', 'marxism-lineage': '马克思主义谱系',
    'economics-lineage': '经济思想谱系', 'econ-part2-lineage': '经济思想谱系下篇',
    'psych-lineage': '心理学思想谱系', 'math-lineage': '数学思想谱系',
    'logic-lineage': '逻辑与论证思想谱系', 'philosophy-lineage': '西方哲学思想谱系',
    'science-lineage': '科学思想谱系', 'social-thought': '社会思想谱系',
    'history-lineage': '历史思想谱系', 'ethics-lineage': '伦理与道德思想谱系',
    'literature-lineage': '文学与语言思想谱系', 'rhetoric-lineage': '修辞与演说思想谱系',
    'education-lineage': '教育思想谱系', 'life-science-lineage': '生命科学思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系', 'politics-lineage': '政治学通论',
    'liberalism-lineage': '自由主义谱系', 'isms-glossary': '政治基础概念1',
    'law-lineage': '法哲学思想谱系', 'eastern-thought-lineage': '东方思想谱系',
    'art-aesthetics-lineage': '艺术与美学思想谱系', 'anthropology-lineage': '人类学思想谱系',
    'media-lineage': '传播与媒介思想谱系', 'military-lineage': '军事与战略思想谱系',
    'ir-lineage': '国际关系思想谱系', 'geo-lineage': '地理与环境思想谱系',
    'religion-lineage': '宗教学与神话', 'astronomy-lineage': '天文学与宇宙学',
    'physics-lineage': '物理学', 'chemistry-lineage': '化学',
    'cs-lineage': '计算机科学', 'linguistics-lineage': '语言学',
    'medicine-lineage': '医学与健康', 'upgrade-summary-2026': 'upgrade-summary-2026',
    '思想图谱系列': '思想图谱系列', 'series-overview': 'series-overview',
}

# 反向校验：确保映射中的中文目录真实存在
for en, cn in en_to_cn.items():
    if cn == en:
        continue
    if not os.path.isdir(os.path.join(dt, cn)):
        print('!! 桌面目录不存在: {} (en={})'.format(cn, en))
        raise SystemExit(1)

vol_dirs = [d for d in os.listdir(ws)
            if os.path.isdir(os.path.join(ws, d))
            and not d.startswith('_') and not d.startswith('.')]


def convert_links(c):
    """工作区链接 ../英文目录/ -> 桌面版 ../中文目录/"""
    for en, cn in en_to_cn.items():
        c = c.replace('../' + en + '/', '../' + cn + '/')
    return c


synced = 0
skipped = 0
for d in sorted(vol_dirs):
    if d == '思想图谱系列':
        continue  # 已单独同步
    wdir = os.path.join(ws, d)
    cdir = os.path.join(dt, en_to_cn.get(d, d))
    for fname in os.listdir(wdir):
        if not fname.endswith('.html') or fname.endswith('.bak'):
            continue
        wf = os.path.join(wdir, fname)
        c = open(wf, encoding='utf-8').read()
        new_c = convert_links(c)
        df = os.path.join(cdir, fname)
        if not os.path.exists(df):
            # 桌面版没有同名文件：新建（如中文名副本不存在则跳过的由后续逻辑处理）
            pass
        if os.path.exists(df):
            bak = df + '.bak'
            if not os.path.exists(bak):
                shutil.copy2(df, bak)
        open(df, 'w', encoding='utf-8').write(new_c)
        synced += 1
        if new_c != c:
            print('  [转换] {}/{}'.format(d, fname))
        else:
            print('  [同步] {}/{}'.format(d, fname))

print()
print('共同步 {} 个文件'.format(synced))

# 额外：桌面版中文名副本（主卷文件）也更新
print()
print('=== 更新桌面版中文名主文件副本 ===')
for en, cn in en_to_cn.items():
    if cn == en:
        continue
    wmain = os.path.join(ws, en, en + '.html')
    if not os.path.exists(wmain):
        continue
    c = open(wmain, encoding='utf-8').read()
    new_c = convert_links(c)
    df = os.path.join(dt, cn, cn + '.html')
    if os.path.exists(df):
        bak = df + '.bak'
        if not os.path.exists(bak):
            shutil.copy2(df, bak)
        open(df, 'w', encoding='utf-8').write(new_c)
        print('  [更新] {}/{}'.format(cn, cn + '.html'))
