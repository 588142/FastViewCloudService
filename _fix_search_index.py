# -*- coding: utf-8 -*-
"""修复 _search_index.json 中的英文路径 → 中文路径"""
import os, re

dt = r'c:\Users\Admin1\Desktop\Trae资料库'

dir_map = {
    'anthropology-lineage': '人类学思想谱系',
    'art-aesthetics-lineage': '艺术与美学思想谱系',
    'astronomy-lineage': '天文学与宇宙学',
    'chemistry-lineage': '化学',
    'cs-lineage': '计算机科学',
    'eastern-thought-lineage': '东方思想谱系',
    'econ-part2-lineage': '经济思想谱系下篇',
    'economics-lineage': '经济思想谱系',
    'education-lineage': '教育思想谱系',
    'ethics-lineage': '伦理与道德思想谱系',
    'geo-lineage': '地理与环境思想谱系',
    'history-lineage': '历史思想谱系',
    'ir-lineage': '国际关系思想谱系',
    'isms-glossary': '政治基础概念1',
    'law-lineage': '法哲学思想谱系',
    'liberalism-lineage': '自由主义谱系',
    'life-science-lineage': '生命科学思想谱系',
    'linguistics-lineage': '语言学',
    'literature-lineage': '文学与语言思想谱系',
    'logic-lineage': '逻辑与论证思想谱系',
    'marxism-lineage': '马克思主义谱系',
    'math-lineage': '数学思想谱系',
    'media-lineage': '传播与媒介思想谱系',
    'medicine-lineage': '医学与健康',
    'military-lineage': '军事与战略思想谱系',
    'philosophy-lineage': '西方哲学思想谱系',
    'physics-lineage': '物理学',
    'politics-lineage': '政治学通论',
    'psych-lineage': '心理学思想谱系',
    'religion-lineage': '宗教学与神话',
    'rhetoric-lineage': '修辞与演说思想谱系',
    'science-lineage': '科学思想谱系',
    'social-thought': '社会思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系',
    'truth-dimensions': '真理的多维图景',
    'bio-lineage': '生命科学思想谱系',
}
file_map = {}
for en, cn in dir_map.items():
    file_map[en + '.html'] = cn + '.html'
file_map['isms-glossary.html'] = '政治基础概念1.html'
file_map['isms-lineage.html'] = '政治基础概念1.html'
file_map['edu-lineage.html'] = '教育思想谱系.html'
file_map['series-overview.html'] = '系列总览.html'
file_map['upgrade-summary-2026.html'] = '升级总结2026.html'
file_map['eastern-thought.html'] = '东方思想谱系.html'

def convert_path(path):
    if '#' in path:
        p, _, a = path.partition('#')
        a = '#' + a
    else:
        p, a = path, ''
    segs = p.rstrip('/').split('/')
    if not segs[-1].lower().endswith('.html'):
        return path
    filename = segs[-1]
    dirs = segs[:-1]
    newdirs = []
    for s in dirs:
        if s in ('..', '.', ''):
            newdirs.append(s)
        elif s in dir_map:
            newdirs.append(dir_map[s])
        else:
            newdirs.append(s)
    newfile = file_map.get(filename, filename)
    return '/'.join(newdirs + [newfile]) + a

fp = os.path.join(dt, '思想图谱系列', '_search_index.json')
c = open(fp, encoding='utf-8').read()
old = c

def repl(m):
    return '"%s"' % convert_path(m.group(1))

# 只匹配含 .html 的字符串值（路径）
c2 = re.sub(r'"([^"]*\.html[^"]*)"', repl, c)

if c2 != c:
    open(fp, 'w', encoding='utf-8').write(c2)
    print('已转换 _search_index.json')

# 验证
c3 = open(fp, encoding='utf-8').read()
en_html = re.findall(r'"\.\./([a-z][a-z-]+)/[a-z][a-z-]*\.html[^"]*"', c3)
remaining = re.findall(r'"\.\./([a-z][a-z-]*)"', c3)
print('剩余英文 .html 路径引用: %d 处' % len(en_html))
for h in sorted(set(remaining))[:10]:
    print('  残留目录: %s' % h)
print('完成' if len(en_html) == 0 else '仍有残留')