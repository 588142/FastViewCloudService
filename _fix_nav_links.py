# -*- coding: utf-8 -*-
"""修复目录页↔各卷跳转断链：
1. 根目录 index.html/主题索引.html/_search_index.json: ../卷名/ → ./卷名/
2. 卷内文件与系列总览: ../思想图谱系列/ → ../ (指向同级根目录)
修改前均生成 .bak 备份
"""
import os, shutil, re

ROOT = r"c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列"

def bak(fp):
    if not os.path.exists(fp + '.bak'):
        shutil.copy2(fp, fp + '.bak')

def fix_root_file(name):
    fp = os.path.join(ROOT, name)
    if not os.path.exists(fp):
        print(f"  !! 不存在: {name}")
        return
    c = open(fp, encoding='utf-8').read()
    n1 = c.count('"../')
    c2 = c.replace('"../', '"./')
    n2 = c2.count("'../")
    c3 = c2.replace("'../", "'./")
    n3 = c3.count('url(../')
    c4 = c3.replace('url(../', 'url(./')
    bak(fp)
    open(fp, 'w', encoding='utf-8').write(c4)
    print(f"  [根] {name}: 双引号../ {n1} -> ./, 单引号../ {n2}, url(../ {n3}")

def fix_vol_files():
    """卷内与 series-overview: ../思想图谱系列/ -> ../"""
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        if rel == '.':
            continue  # 根目录单独处理
        for f in fn:
            if not f.endswith('.html'):
                continue
            fp = os.path.join(dp, f)
            c = open(fp, encoding='utf-8').read()
            if '../思想图谱系列/' not in c:
                continue
            cnt = c.count('../思想图谱系列/')
            bak(fp)
            open(fp, 'w', encoding='utf-8').write(c.replace('../思想图谱系列/', '../'))
            n += 1
            print(f"  [卷] {rel}\\{f}: 修复 {cnt} 处")
    return n

print("== 1. 根目录文件 ==")
fix_root_file('index.html')
fix_root_file('主题索引.html')
fix_root_file('_search_index.json')
print("== 2. 卷内文件 ==")
fix_vol_files()
print("== 完成 ==")
