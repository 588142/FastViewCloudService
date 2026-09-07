# -*- coding: utf-8 -*-
"""
将 Trae资料库 中所有 HTML 文件改为中文名 + 同步最新版 思想图谱系列/series-overview
"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# ===== 目录 → (英文文件, 中文文件) 映射 =====
pairs = [
    ('人类学思想谱系', 'anthropology-lineage.html', '人类学思想谱系.html'),
    ('传播与媒介思想谱系', 'media-lineage.html', '传播与媒介思想谱系.html'),
    ('伦理与道德思想谱系', 'ethics-lineage.html', '伦理与道德思想谱系.html'),
    ('修辞与演说思想谱系', 'rhetoric-lineage.html', '修辞与演说思想谱系.html'),
    ('军事与战略思想谱系', 'military-lineage.html', '军事与战略思想谱系.html'),
    ('化学', 'chemistry-lineage.html', '化学.html'),
    ('医学与健康', 'medicine-lineage.html', '医学与健康.html'),
    ('历史思想谱系', 'history-lineage.html', '历史思想谱系.html'),
    ('国际关系思想谱系', 'ir-lineage.html', '国际关系思想谱系.html'),
    ('地理与环境思想谱系', 'geo-lineage.html', '地理与环境思想谱系.html'),
    ('天文学与宇宙学', 'astronomy-lineage.html', '天文学与宇宙学.html'),
    ('宗教学与神话', 'religion-lineage.html', '宗教学与神话.html'),
    ('心理学思想谱系', 'psych-lineage.html', '心理学思想谱系.html'),
    ('政治学通论', 'politics-lineage.html', '政治学通论.html'),
    ('教育思想谱系', 'education-lineage.html', '教育思想谱系.html'),
    ('数学思想谱系', 'math-lineage.html', '数学思想谱系.html'),
    ('文学与语言思想谱系', 'literature-lineage.html', '文学与语言思想谱系.html'),
    ('法哲学思想谱系', 'law-lineage.html', '法哲学思想谱系.html'),
    ('物理学', 'physics-lineage.html', '物理学.html'),
    ('生命科学思想谱系', 'life-science-lineage.html', '生命科学思想谱系.html'),
    ('真理的多维图景', 'truth-dimensions.html', '真理的多维图景.html'),
    ('社会思想谱系', 'social-thought.html', '社会思想谱系.html'),
    ('科学思想谱系', 'science-lineage.html', '科学思想谱系.html'),
    ('科技与人工智能思想谱系', 'tech-ai-lineage.html', '科技与人工智能思想谱系.html'),
    ('经济思想谱系', 'economics-lineage.html', '经济思想谱系.html'),
    ('经济思想谱系下篇', 'econ-part2-lineage.html', '经济思想谱系下篇.html'),
    ('自由主义谱系', 'liberalism-lineage.html', '自由主义谱系.html'),
    ('艺术与美学思想谱系', 'art-aesthetics-lineage.html', '艺术与美学思想谱系.html'),
    ('西方哲学思想谱系', 'philosophy-lineage.html', '西方哲学思想谱系.html'),
    ('计算机科学', 'cs-lineage.html', '计算机科学.html'),
    ('语言学', 'linguistics-lineage.html', '语言学.html'),
    ('逻辑与论证思想谱系', 'logic-lineage.html', '逻辑与论证思想谱系.html'),
    ('马克思主义谱系', 'marxism-lineage.html', '马克思主义谱系.html'),
    ('东方思想谱系', 'eastern-thought-lineage.html', '东方思想谱系.html'),
    ('政治基础概念1', 'isms-glossary.html', '政治基础概念1.html'),
    ('政治基础概念1', 'isms-lineage.html', None),  # 额外英文 → 删除
    ('生命科学思想谱系', 'bio-lineage.html', None),  # 额外英文 → 删除
]

# ===== 1. 删除英文名文件 + 清理 .bak =====
print('=== 1. 删除英文名文件 & .bak 清理 ===')
del_count = 0
bak_count = 0
for d, en, cn in pairs:
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    # 删除英文名文件
    ep = os.path.join(dp, en)
    if os.path.exists(ep):
        os.remove(ep)
        del_count += 1
        print(f'  ❌ 删除 {d}/{en}')
    # 如果 cn 为 None，说明这个英文文件没有中文对应（额外文件），已被删除
    # 清理 .bak
    for f in os.listdir(dp):
        if f.endswith('.bak') or f.endswith('.bak2') or f.endswith('.bak3') or f.endswith('.bak4'):
            os.remove(os.path.join(dp, f))
            bak_count += 1
print(f'  共删除 {del_count} 个英文名文件, {bak_count} 个 .bak 文件')

# ===== 2. 同步最新版（从工作区）到中文名文件 =====
print()
print('=== 2. 同步最新版到中文名文件 ===')
ws_to_cn = {
    # 7 个无中文名的简单卷：工作区目录 → 桌面版目录 → 中文名
    ('chemistry', '化学', '化学.html'),
    ('medicine', '医学与健康', '医学与健康.html'),
    ('astronomy', '天文学与宇宙学', '天文学与宇宙学.html'),
    ('religion', '宗教学与神话', '宗教学与神话.html'),
    ('physics', '物理学', '物理学.html'),
    ('cs', '计算机科学', '计算机科学.html'),
    ('linguistics', '语言学', '语言学.html'),
}

# 先同步所有已有中文名的卷
for d, en, cn in pairs:
    if cn is None:
        continue
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    # 从工作区复制最新版
    # 找到工作区对应的目录名
    for wsd in os.listdir(ws):
        wsd_path = os.path.join(ws, wsd)
        if not os.path.isdir(wsd_path):
            continue
        wf = os.path.join(wsd_path, en)
        if os.path.exists(wf):
            # 复制到桌面版中文名
            src = wf
            dst = os.path.join(dp, cn)
            shutil.copy2(src, dst)
            size = os.path.getsize(dst) // 1024
            print(f'  ✅ {d}/{cn} ({size}KB)')
            break

# 同步 7 个简单卷（从工作区目录复制到桌面版目录，创建中文名）
for ws_dir, dt_dir, cn_file in ws_to_cn:
    src = os.path.join(ws, ws_dir, ws_dir + '-lineage.html')
    if not os.path.exists(src):
        src = os.path.join(ws, ws_dir, ws_dir + '.html')
    if not os.path.exists(src):
        print(f'  !! 未找到工作区源: {ws_dir}')
        continue
    dp = os.path.join(dt, dt_dir)
    if not os.path.isdir(dp):
        print(f'  !! 桌面版目录不存在: {dt_dir}')
        continue
    dst = os.path.join(dp, cn_file)
    shutil.copy2(src, dst)
    size = os.path.getsize(dst) // 1024
    print(f'  ✅ {dt_dir}/{cn_file} ({size}KB，从工作区新建)')

# ===== 3. 同步 思想图谱系列 最新版 =====
print()
print('=== 3. 同步 思想图谱系列 最新版 ===')
ws_series = os.path.join(ws, '思想图谱系列')
dt_series = os.path.join(dt, '思想图谱系列')
for f in ['index.html', '阅读指南.html', '主题索引.html', '人物索引.html']:
    src = os.path.join(ws_series, f)
    if not os.path.exists(src):
        print(f'  !! 工作区源不存在: {f}')
        continue
    dst = os.path.join(dt_series, f)
    if os.path.exists(dst):
        bak = dst + '.bak'
        shutil.copy2(dst, bak)
    shutil.copy2(src, dst)
    size = os.path.getsize(dst) // 1024
    print(f'  ✅ 思想图谱系列/{f} ({size}KB)')

# ===== 4. 同步 series-overview 最新版 =====
print()
print('=== 4. 同步 series-overview 最新版 ===')
dt_so = os.path.join(dt, 'series-overview')
# 先删除英文名
so_en = os.path.join(dt_so, 'series-overview.html')
if os.path.exists(so_en):
    os.remove(so_en)
    print('  ❌ 删除 series-overview/series-overview.html')
# 清理 .bak
for f in os.listdir(dt_so):
    if f.endswith('.bak'):
        os.remove(os.path.join(dt_so, f))
# 从工作区复制最新版
src = os.path.join(ws, 'series-overview', 'series-overview.html')
dst = os.path.join(dt_so, '系列总览.html')
shutil.copy2(src, dst)
size = os.path.getsize(dst) // 1024
print(f'  ✅ series-overview/系列总览.html ({size}KB)')

# ===== 5. 同步 upgrade-summary-2026 =====
print()
print('=== 5. 同步 upgrade-summary-2026 ===')
dt_us = os.path.join(dt, 'upgrade-summary-2026')
us_en = os.path.join(dt_us, 'upgrade-summary-2026.html')
if os.path.exists(us_en):
    os.remove(us_en)
    print('  ❌ 删除 upgrade-summary-2026/upgrade-summary-2026.html')
for f in os.listdir(dt_us):
    if f.endswith('.bak'):
        os.remove(os.path.join(dt_us, f))
src = os.path.join(ws, 'upgrade-summary-2026', 'upgrade-summary-2026.html')
dst = os.path.join(dt_us, '升级总结2026.html')
shutil.copy2(src, dst)
size = os.path.getsize(dst) // 1024
print(f'  ✅ upgrade-summary-2026/升级总结2026.html ({size}KB)')

# ===== 6. 清理桌面版根目录独立文件 =====
print()
print('=== 6. 清理桌面版根目录 ===')
for f in ['index.html', 'index.html.bak', '主题索引.html', '人物索引.html', '阅读指南.html']:
    fp = os.path.join(dt, f)
    if os.path.exists(fp):
        os.remove(fp)
        print(f'  ❌ 删除 {f}')

# ===== 7. 验证 =====
print()
print('=== 7. 验证结果 ===')
remaining_bak = 0
remaining_en = 0
en_names = set(en for _, en, _ in pairs if en)
for d in os.listdir(dt):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    for f in os.listdir(dp):
        if f.endswith('.bak') or f.endswith('.bak2') or f.endswith('.bak3') or f.endswith('.bak4'):
            remaining_bak += 1
            print(f'  ⚠️ 残留 .bak: {d}/{f}')
        elif f.endswith('.html') and f in en_names:
            remaining_en += 1
            print(f'  ⚠️ 残留英文名: {d}/{f}')

if remaining_bak == 0 and remaining_en == 0:
    print('  ✅ 全部清理完毕，无残留英文名文件或 .bak 文件')
else:
    print(f'  ⚠️ 残留 {remaining_en} 个英文名文件, {remaining_bak} 个 .bak 文件')

# 检查每个目录都有中文名文件
missing = []
for d in os.listdir(dt):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    has_cn = False
    for f in os.listdir(dp):
        if f.endswith('.html') and not f.endswith('.bak'):
            # 检查是否包含中文
            if any('\u4e00' <= c <= '\u9fff' for c in f):
                has_cn = True
                break
    if not has_cn:
        missing.append(d)
if missing:
    print(f'  ⚠️ 缺少中文名文件的目录: {missing}')
else:
    print('  ✅ 所有目录均有中文名文件')

print()
print('全部完成！')