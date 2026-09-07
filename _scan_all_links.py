# -*- coding: utf-8 -*-
"""全库断链扫描：检查每个HTML内所有相对链接是否可解析"""
import os, re, json, sys

TARGETS = [
    (r"c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列", "工作区"),
    (r"c:\Users\Admin1\Desktop\Trae资料库", "桌面版"),
    (r"C:\Users\Admin1\OneDrive\思想图谱系列\Trae资料库", "OneDrive"),
]

def check_dir(base, label):
    print(f"\n===== {label}: {base} =====")
    total_bad = 0
    files = 0
    for dp, dn, fn in os.walk(base):
        # 跳过 _shared 与 assets 内部文件检查（资源目录单独处理）
        rel = os.path.relpath(dp, base)
        parts = rel.split(os.sep)
        if any(p in ('_shared', 'assets') for p in parts):
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            fp = os.path.join(dp, f)
            files += 1
            try:
                c = open(fp, encoding='utf-8').read()
            except Exception:
                continue
            hrefs = re.findall(r'(?:href|src)="([^"]+)"', c)
            bad = []
            for h in hrefs:
                if h.startswith(('#', 'http://', 'https://', 'mailto:', 'data:', 'javascript:', 'tel:')):
                    continue
                if h.startswith('http'):
                    continue
                # 去掉锚点
                path = h.split('#')[0]
                if not path:
                    continue
                # 解析目标
                tgt = os.path.normpath(os.path.join(dp, path))
                if not os.path.exists(tgt):
                    bad.append(h)
            if bad:
                total_bad += len(bad)
                print(f"  [{f}] 断链 {len(bad)}")
                for b in bad[:8]:
                    print(f"      -> {b}")
                if len(bad) > 8:
                    print(f"      ... 等 {len(bad)} 条")
    print(f"  -- {label}: 检查HTML {files} 个, 总断链 {total_bad}")
    return total_bad

total = 0
for base, label in TARGETS:
    if os.path.isdir(base):
        total += check_dir(base, label)
    else:
        print(f"\n===== {label} 不存在: {base}")
print(f"\n########## 总断链: {total} ##########")
