# -*- coding: utf-8 -*-
"""修复 7 个简单卷的同步 + 清理残留 .bak + 检查 index.html"""
import os, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# ===== 1. 修复 7 个简单卷（工作区目录名带 -lineage 后缀） =====
print('=== 1. 修复简单卷同步 ===')
ws_to_cn = [
    ('chemistry-lineage', '化学', '化学.html'),
    ('medicine-lineage', '医学与健康', '医学与健康.html'),
    ('astronomy-lineage', '天文学与宇宙学', '天文学与宇宙学.html'),
    ('religion-lineage', '宗教学与神话', '宗教学与神话.html'),
    ('physics-lineage', '物理学', '物理学.html'),
    ('cs-lineage', '计算机科学', '计算机科学.html'),
    ('linguistics-lineage', '语言学', '语言学.html'),
]
for ws_dir, dt_dir, cn_file in ws_to_cn:
    src = os.path.join(ws, ws_dir, ws_dir + '.html')
    if not os.path.exists(src):
        print(f'  !! 源文件不存在: {src}')
        continue
    dp = os.path.join(dt, dt_dir)
    if not os.path.isdir(dp):
        print(f'  !! 桌面目录不存在: {dp}')
        continue
    dst = os.path.join(dp, cn_file)
    shutil.copy2(src, dst)
    size = os.path.getsize(dst) // 1024
    print(f'  ✅ {dt_dir}/{cn_file} ({size}KB)')

# ===== 2. 检查 思想图谱系列/index.html =====
print()
print('=== 2. 检查 思想图谱系列/index.html ===')
ws_i = os.path.join(ws, '思想图谱系列', 'index.html')
if os.path.exists(ws_i):
    size = os.path.getsize(ws_i) // 1024
    dt_i = os.path.join(dt, '思想图谱系列', 'index.html')
    shutil.copy2(ws_i, dt_i)
    print(f'  ✅ 思想图谱系列/index.html ({size}KB) 已同步')
else:
    print(f'  !! 工作区不存在: {ws_i}')
    # 列出实际文件
    for f in os.listdir(os.path.join(ws, '思想图谱系列')):
        print(f'    {f}')

# ===== 3. 清理残留 .bak =====
print()
print('=== 3. 清理残留 .bak ===')
for d in ['思想图谱系列']:
    dp = os.path.join(dt, d)
    for f in os.listdir(dp):
        if f.endswith('.bak'):
            os.remove(os.path.join(dp, f))
            print(f'  ❌ 删除 {d}/{f}')

# ===== 4. 最终验证 =====
print()
print('=== 4. 最终验证 ===')
en_samples = ['anthropology-lineage.html', 'chemistry-lineage.html', 'cs-lineage.html',
              'series-overview.html', 'upgrade-summary-2026.html', 'logic-lineage.html']
bak_found = 0
en_found = 0
all_dirs = []
for d in os.listdir(dt):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    all_dirs.append(d)
    for f in os.listdir(dp):
        if f.endswith('.bak'):
            bak_found += 1
            print(f'  ⚠️ .bak: {d}/{f}')
        elif f in en_samples:
            en_found += 1
            print(f'  ⚠️ 英文: {d}/{f}')

print(f'  目录数: {len(all_dirs)}')
print(f'  残留英文: {en_found}, 残留.bak: {bak_found}')
if bak_found == 0 and en_found == 0:
    print('  ✅ 全部清理完毕')

# 列出所有目录和中文名文件
print()
print('=== 中文名文件清单 ===')
for d in sorted(all_dirs):
    dp = os.path.join(dt, d)
    cn_files = [f for f in os.listdir(dp) if f.endswith('.html') and not f.endswith('.bak')
                and any('\u4e00' <= c <= '\u9fff' for c in f)]
    if cn_files:
        print(f'  📁 {d}/  → {cn_files}')
    else:
        print(f'  ⚠️ {d}/  → 无中文名文件')

print()
print('全部完成！')