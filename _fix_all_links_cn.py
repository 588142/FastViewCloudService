# -*- coding: utf-8 -*-
"""
修复桌面版 Trae资料库 的跨卷链接：
  英文目录/英文文件名 → 中文目录/中文文件名
并同步今天更新的最新版文件，删除副本目录。
"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# ===== 英文目录 → 中文目录（series-overview / upgrade-summary-2026 目录名不变，不在此表） =====
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
}

# ===== 英文文件名 → 中文文件名 =====
file_map = {}
for en, cn in dir_map.items():
    file_map[en + '.html'] = cn + '.html'
# 特殊文件
file_map['isms-glossary.html'] = '政治基础概念1.html'
file_map['isms-lineage.html'] = '政治基础概念1.html'
file_map['bio-lineage.html'] = '生命科学思想谱系.html'
file_map['series-overview.html'] = '系列总览.html'
file_map['upgrade-summary-2026.html'] = '升级总结2026.html'

def convert_href(href):
    """把 href 中的英文目录/文件名转为中文"""
    if href.startswith(('http://', 'https://', 'mailto:', '#', 'javascript:')):
        return href
    # 分离锚点
    if '#' in href:
        path, _, anchor = href.partition('#')
        anchor = '#' + anchor
    else:
        path, anchor = href, ''
    if not path.lower().endswith('.html'):
        return href
    segments = path.rstrip('/').split('/')
    filename = segments[-1]
    dirs = segments[:-1]
    new_dirs = []
    for seg in dirs:
        if seg in ('..', '.', ''):
            new_dirs.append(seg)
        elif seg in dir_map:
            new_dirs.append(dir_map[seg])
        else:
            new_dirs.append(seg)
    new_filename = file_map.get(filename, filename)
    return '/'.join(new_dirs + [new_filename]) + anchor

# ===== 1. 删除副本目录 =====
print('=== 1. 删除副本目录 ===')
removed = 0
for d in os.listdir(dt):
    if '副本' in d or ' - 副本' in d or ' - Copy' in d:
        p = os.path.join(dt, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
            removed += 1
            print('  删除: %s' % d)
print('  共删除 %d 个副本目录' % removed)

# ===== 2. 同步今天更新(09-07)的最新版文件 =====
print()
print('=== 2. 同步今天更新的最新版 ===')
today_sync = [
    ('econ-part2-lineage', 'econ-part2-lineage.html', '经济思想谱系下篇', '经济思想谱系下篇.html'),
    ('economics-lineage', 'economics-lineage.html', '经济思想谱系', '经济思想谱系.html'),
    ('liberalism-lineage', 'liberalism-lineage.html', '自由主义谱系', '自由主义谱系.html'),
    ('logic-lineage', 'logic-lineage.html', '逻辑与论证思想谱系', '逻辑与论证思想谱系.html'),
    ('marxism-lineage', 'marxism-lineage.html', '马克思主义谱系', '马克思主义谱系.html'),
    ('math-lineage', 'math-lineage.html', '数学思想谱系', '数学思想谱系.html'),
    ('psych-lineage', 'psych-lineage.html', '心理学思想谱系', '心理学思想谱系.html'),
    ('series-overview', 'series-overview.html', 'series-overview', '系列总览.html'),
    ('social-thought', 'social-thought.html', '社会思想谱系', '社会思想谱系.html'),
    ('truth-dimensions', 'truth-dimensions.html', '真理的多维图景', '真理的多维图景.html'),
]
for wd, wf, dd, df in today_sync:
    src = os.path.join(ws, wd, wf)
    dst = os.path.join(dt, dd, df)
    if os.path.exists(src) and os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
        print('  ✅ %s/%s (%d KB)' % (dd, df, os.path.getsize(dst)//1024))
    else:
        print('  !! 跳过 %s/%s (源不存在)' % (wd, wf))

# 同步 主题索引.html
shutil.copy2(os.path.join(ws, '思想图谱系列', '主题索引.html'),
             os.path.join(dt, '思想图谱系列', '主题索引.html'))
print('  ✅ 思想图谱系列/主题索引.html')

# ===== 3. 遍历桌面版所有 HTML，转换链接 =====
print()
print('=== 3. 转换全部跨卷链接（英→中） ===')
total_changed = 0
total_files = 0
for d in os.listdir(dt):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    for f in os.listdir(dp):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        c = open(fp, encoding='utf-8').read()
        old = c
        def repl(m):
            return 'href="%s"' % convert_href(m.group(1))
        c = re.sub(r'href="([^"]*)"', repl, c)
        if c != old:
            open(fp, 'w', encoding='utf-8').write(c)
            n = len(re.findall(r'href="[^"]*"', old)) - len(re.findall(r'href="[^"]*"', c))
            total_files += 1
            total_changed += 1
print('  修改了 %d 个文件' % total_files)

# ===== 4. 验证零断链 =====
print()
print('=== 4. 验证断链 ===')
total_broken = 0
broken_files = []
for d in os.listdir(dt):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    for f in os.listdir(dp):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        c = open(fp, encoding='utf-8').read()
        links = re.findall(r'href="(\.\.[^"]*)"', c)
        broken = [l for l in links if not os.path.exists(os.path.normpath(os.path.join(dp, l)))]
        if broken:
            total_broken += len(broken)
            broken_files.append((d, f, broken[:5], len(broken)))
print('  总断链: %d' % total_broken)
for d, f, bs, n in broken_files:
    print('  %s/%s: %d 断链' % (d, f, n))
    for b in bs:
        print('    -> %s' % b)

print()
print('全部完成！' if total_broken == 0 else '仍存在断链，需继续排查！')