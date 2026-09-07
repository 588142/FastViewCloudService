# -*- coding: utf-8 -*-
"""同步 目录页/主题索引 到桌面版：英文目录 -> 中文目录转换"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# 工作区英文目录 -> 桌面版中文目录
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
    '思想图谱系列': '思想图谱系列',
    'series-overview': 'series-overview',
}


def convert(c, ws_dir):
    """把工作区内容中的 ../英文目录/ 转换为 ../中文目录/"""
    used = []
    for en, cn in en_to_cn.items():
        pat = '../' + en + '/'
        if pat in c:
            # 校验工作区目录确实存在
            if not os.path.isdir(os.path.join(ws, en)):
                print('    !! 工作区目录不存在: {}'.format(en))
            c = c.replace(pat, '../' + cn + '/')
            used.append(en)
    return c, used


total = 0
for fname in ['index.html', '主题索引.html']:
    src = os.path.join(ws, '思想图谱系列', fname)
    dst = os.path.join(dt, '思想图谱系列', fname)
    c = open(src, encoding='utf-8').read()
    new_c, used = convert(c, fname)
    # 备份桌面旧版
    bak = dst + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(dst, bak)
    open(dst, 'w', encoding='utf-8').write(new_c)
    total += 1
    print('[已同步] {} -> 桌面版 (转换目录: {})'.format(fname, len(used)))

print()
print('=== 验证转换后桌面版断链 ===')
for fname in ['index.html', '主题索引.html']:
    fp = os.path.join(dt, '思想图谱系列', fname)
    c = open(fp, encoding='utf-8').read()
    links = re.findall(r'href="\.\./([^"]*)"', c)
    broken = [l for l in sorted(set(links)) if not os.path.exists(os.path.normpath(os.path.join(dt, '思想图谱系列', '..', l)))]
    chinese = sum(1 for l in links if not re.match(r'^[a-z]', l.split('/')[0]))
    print('  {}: {}链接, 中文目录{}个, 断链{}个'.format(fname, len(links), chinese, len(broken)))
    for b in broken:
        print('    BROKEN -> ../{}'.format(b))

print()
print('=== 确认旧文件名链接已清除 ===')
for fname in ['index.html', '主题索引.html']:
    fp = os.path.join(dt, '思想图谱系列', fname)
    c = open(fp, encoding='utf-8').read()
    for old in ['econ-thought.html', 'art-aesthetics.html', 'eastern-thought.html', 'edu-lineage.html']:
        if old in c:
            print('  !! {} 仍引用 {}'.format(fname, old))
    else:
        pass
print('检查完成')
