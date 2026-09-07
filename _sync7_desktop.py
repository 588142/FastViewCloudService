# -*- coding: utf-8 -*-
"""同步7个标星卷到桌面版：复制+链接路径转换(英文目录→中文目录)+验证"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# (工作区目录, 桌面版目录, 桌面版中文文件名)
pairs = [
    ('truth-dimensions',   '真理的多维图景',    '真理的多维图景.html'),
    ('marxism-lineage',    '马克思主义谱系',    '马克思主义谱系.html'),
    ('economics-lineage',  '经济思想谱系',      '经济思想谱系.html'),
    ('econ-part2-lineage', '经济思想谱系下篇',  '经济思想谱系下篇.html'),
    ('psych-lineage',      '心理学思想谱系',    '心理学思想谱系.html'),
    ('math-lineage',       '数学思想谱系',      '数学思想谱系.html'),
    ('logic-lineage',      '逻辑与论证思想谱系','逻辑与论证思想谱系.html'),
]

# 跨卷链接目录映射：工作区英文目录 → 桌面版中文目录
dir_map = {
    'econ-part2-lineage': '经济思想谱系下篇',
    'economics-lineage': '经济思想谱系',
    'education-lineage': '教育思想谱系',
    'ethics-lineage': '伦理与道德思想谱系',
    'history-lineage': '历史思想谱系',
    'isms-glossary': '政治基础概念1',
    'liberalism-lineage': '自由主义谱系',
    'life-science-lineage': '生命科学思想谱系',
    'literature-lineage': '文学与语言思想谱系',
    'logic-lineage': '逻辑与论证思想谱系',
    'marxism-lineage': '马克思主义谱系',
    'math-lineage': '数学思想谱系',
    'philosophy-lineage': '西方哲学思想谱系',
    'politics-lineage': '政治学通论',
    'psych-lineage': '心理学思想谱系',
    'rhetoric-lineage': '修辞与演说思想谱系',
    'science-lineage': '科学思想谱系',
    'social-thought': '社会思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系',
    'truth-dimensions': '真理的多维图景',
    'series-overview': 'series-overview',
    '思想图谱系列': '思想图谱系列',
}

def convert_links(content):
    """把 ../英文目录/ 转换为 ../中文目录/"""
    for en, cn in dir_map.items():
        content = content.replace(f'../{en}/', f'../{cn}/')
    return content

for wd, dd, dcn in pairs:
    src = os.path.join(ws, wd, wd + '.html')
    c = open(src, encoding='utf-8').read()
    c_cnv = convert_links(c)

    dst_dir = os.path.join(dt, dd)
    if not os.path.isdir(dst_dir):
        print(f'!! 桌面目录不存在: {dst_dir}')
        continue

    # 英文名文件
    dst_en = os.path.join(dst_dir, wd + '.html')
    # 中文名文件
    dst_cn = os.path.join(dst_dir, dcn)

    for dst in [dst_en, dst_cn]:
        if os.path.exists(dst):
            bak = dst + '.bak4'
            if not os.path.exists(bak):
                shutil.copy2(dst, bak)
        open(dst, 'w', encoding='utf-8').write(c_cnv)

    # === 验证 ===
    problems = []
    # 1. 链接目标存在
    for cl in re.findall(r'href="\.\./([^"]*)"', c_cnv):
        full = os.path.normpath(os.path.join(dst_dir, '..', cl))
        if not os.path.exists(full):
            problems.append(f'断链: {cl}')
    # 2. 无残留英文目录链接（排除映射到自身的）
    for en, cn in dir_map.items():
        if en == cn:
            continue
        if f'../{en}/' in c_cnv:
            problems.append(f'残留英文目录链接: {en}')
    # 3. 字符数一致
    n_cnv = len(c_cnv)
    n_dst = len(open(dst_en, encoding='utf-8').read())
    if n_cnv != n_dst:
        problems.append('文件写入不一致')

    status = '✅' if not problems else '⚠️'
    print(f'{dd:12s} | {os.path.getsize(dst_en)//1024:>4d}KB | {status}')
    for p in problems[:5]:
        print(f'    - {p}')

print('\n桌面同步完成')
