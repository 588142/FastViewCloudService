# -*- coding: utf-8 -*-
"""修复所有断链"""
import re, os, glob

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

# 文件名映射表：错误文件名 → 正确文件名
fix_map = {
    'econ-thought.html': 'economics-lineage.html',
    'eastern-thought.html': 'eastern-thought-lineage.html',
    'art-aesthetics.html': 'art-aesthetics-lineage.html',
    'edu-lineage.html': 'education-lineage.html',
}

total_fixes = 0

# 1. 修复 思想图谱系列/index.html 中的链接
rd = os.path.join(ws, '思想图谱系列')
for f in ['index.html', '主题索引.html', '阅读指南.html']:
    fp = os.path.join(rd, f)
    if not os.path.exists(fp):
        print(f'  {f} 不存在')
        continue
    c = open(fp, encoding='utf-8').read()
    old = c
    for wrong, correct in fix_map.items():
        # 替换所有 ../dir/wrong 为 ../dir/correct
        c = re.sub(rf'(\.\./[^/]+/){re.escape(wrong)}', rf'\1{correct}', c)
    if c != old:
        # 备份
        with open(fp + '.bak', 'w', encoding='utf-8') as fb:
            fb.write(old)
        open(fp, 'w', encoding='utf-8').write(c)
        diff = c.count('href="') - old.count('href="')
        print(f'  ✅ {f}: 已修复')
        total_fixes += 1
    else:
        print(f'  {f}: 无变化')


# 2. 修复 series-overview 中的人物索引链接
fp = os.path.join(ws, 'series-overview', 'series-overview.html')
c = open(fp, encoding='utf-8').read()
old = c
# 人物索引在 思想图谱系列 目录下
c = c.replace('../思想图谱系列/人物索引.html', '../思想图谱系列/主题索引.html')
if c != old:
    with open(fp + '.bak', 'w', encoding='utf-8') as fb:
        fb.write(old)
    open(fp, 'w', encoding='utf-8').write(c)
    print(f'  ✅ series-overview: 人物索引链接已修复 -> 主题索引.html')
    total_fixes += 1
else:
    print(f'  series-overview: 无变化')


# 3. 修复 social-thought 中的链接
fp = os.path.join(ws, 'social-thought', 'social-thought.html')
c = open(fp, encoding='utf-8').read()
old = c
c = c.replace('../economics-lineage/econ-thought.html', '../economics-lineage/economics-lineage.html')
if c != old:
    with open(fp + '.bak', 'w', encoding='utf-8') as fb:
        fb.write(old)
    open(fp, 'w', encoding='utf-8').write(c)
    print(f'  ✅ social-thought: econ-thought.html 已修复 -> economics-lineage.html')
    total_fixes += 1
else:
    print(f'  social-thought: 无变化')


# 4. 验证修复结果
print(f'\n=== 验证修复 ===')
for vol_dir in os.listdir(ws):
    if vol_dir.startswith('_') or vol_dir.startswith('.'):
        continue
    vp = os.path.join(ws, vol_dir)
    if not os.path.isdir(vp):
        continue
    htmls = glob.glob(os.path.join(vp, '*.html'))
    for hf in htmls:
        c = open(hf, encoding='utf-8').read()
        cross_links = re.findall(r'href="\.\./([^"]*)"', c)
        for cl in cross_links:
            full = os.path.normpath(os.path.join(vp, '..', cl))
            if not os.path.exists(full):
                print(f'  ❌ 仍有断链: {vol_dir}/{os.path.basename(hf)} -> ../{cl}')

print(f'\n总修复数: {total_fixes}')
print('修复完成')