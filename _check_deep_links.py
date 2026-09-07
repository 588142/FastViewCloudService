# -*- coding: utf-8 -*-
"""深度检查：主题索引和各卷内部的链接"""
import re, os

BASE = r"C:\Users\Admin1\Documents\FastViewCloudService"
GUIDE_DIR = os.path.join(BASE, "思想图谱系列")

# 加载 volumes_data.json 获取实际目录名
import json
with open(os.path.join(BASE, "volumes_data.json"), "r", encoding="utf-8") as f:
    VOLUMES = json.load(f)

# 构建 dir -> 合法文件列表的映射
valid_files = {}
for v in VOLUMES:
    d = v["dir"]
    valid_files[d] = set()
    dir_path = os.path.join(BASE, d)
    if os.path.exists(dir_path):
        for fn in os.listdir(dir_path):
            if fn.endswith(".html"):
                valid_files[d].add(fn)

print("=" * 60)
print("1. 主题索引.html 链接检查")
print("=" * 60)

topic_idx = os.path.join(GUIDE_DIR, "主题索引.html")
if os.path.exists(topic_idx):
    with open(topic_idx, "r", encoding="utf-8") as f:
        content = f.read()
    links = re.findall(r'href="\.\./([^"]+)"', content)
    broken = []
    for link in sorted(set(links)):
        parts = link.split("/", 1)
        if len(parts) == 2:
            d, fn = parts
            if d in valid_files and fn in valid_files[d]:
                pass
            else:
                target = os.path.join(BASE, link)
                if not os.path.exists(target):
                    broken.append(link)
    if broken:
        for b in broken:
            print(f"  ✗ 断裂: {b}")
    else:
        print(f"  ✓ 全部 {len(set(links))} 个链接有效")
else:
    print("  ✗ 主题索引.html 不存在")

print("\n" + "=" * 60)
print("2. 各卷内部交叉引用链接检查")
print("=" * 60)

cross_vol_links = []
for v in VOLUMES:
    d = v["dir"]
    vol_path = os.path.join(BASE, d)
    if not os.path.exists(vol_path):
        continue
    for fn in os.listdir(vol_path):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(vol_path, fn)
        with open(fp, "r", encoding="utf-8") as fh:
            c = fh.read()
        # 找到指向其他卷的链接
        refs = re.findall(r'href="\.\./([^"]+)"', c)
        for ref in refs:
            parts = ref.split("/", 1)
            if len(parts) == 2:
                ref_dir, ref_fn = parts
                if ref_dir != d:  # 跨卷引用
                    cross_vol_links.append((d, fn, ref))

# 检查跨卷引用
broken_refs = []
for src_dir, src_fn, ref in set(cross_vol_links):
    target = os.path.join(BASE, ref)
    if not os.path.exists(target):
        broken_refs.append((src_dir, src_fn, ref))

if broken_refs:
    print(f"发现 {len(broken_refs)} 个断裂的跨卷引用:\n")
    for src_dir, src_fn, ref in broken_refs:
        print(f"  ✗ {src_dir}/{src_fn} -> {ref}")
else:
    total = len(set(cross_vol_links))
    print(f"  ✓ 全部 {total} 个跨卷引用有效")

print("\n" + "=" * 60)
print("3. 桌面版同步检查")
print("=" * 60)

desktop = os.path.join(BASE, "..", "..", "Desktop", "Trae资料库", "index.html")
desktop_path = os.path.abspath(desktop)
if os.path.exists(desktop_path):
    ws_size = os.path.getsize(os.path.join(GUIDE_DIR, "index.html"))
    dt_size = os.path.getsize(desktop_path)
    print(f"  工作区: {ws_size} 字节")
    print(f"  桌面:   {dt_size} 字节")
    print(f"  {'✓ 同步一致' if ws_size == dt_size else '✗ 大小不一致'}")
else:
    print(f"  ✗ 桌面文件不存在: {desktop_path}")

print("\n" + "=" * 60)
print("4. 阅读指南.html(旧版) 链接检查")
print("=" * 60)

old_guide = os.path.join(GUIDE_DIR, "阅读指南.html")
if os.path.exists(old_guide):
    with open(old_guide, "r", encoding="utf-8") as f:
        content = f.read()
    old_links = re.findall(r'href="\.\./([^"]+)"', content)
    old_broken = []
    for link in sorted(set(old_links)):
        target = os.path.join(BASE, link)
        if not os.path.exists(target):
            old_broken.append(link)
    if old_broken:
        for b in old_broken:
            print(f"  ✗ 旧版断裂: {b}")
    else:
        print(f"  ✓ 旧版全部 {len(set(old_links))} 个链接有效")
else:
    print("  - 旧版文件不存在")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)