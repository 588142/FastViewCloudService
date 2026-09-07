# -*- coding: utf-8 -*-
import os, re, json

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列\逻辑与论证思想谱系\逻辑与论证思想谱系.html'
c = open(fp, encoding='utf-8').read()
print('=== 逻辑卷 外部库引用 ===')
for m in re.finditer(r'<script[^>]*src="([^"]+)"', c):
    print(m.group(1))
print()
print('=== _shared 内容 ===')
sh = r'c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列\逻辑与论证思想谱系\_shared'
if os.path.isdir(sh):
    for dp, dn, fn in os.walk(sh):
        for f in fn:
            p = os.path.join(dp, f)
            print(os.path.relpath(p, sh), os.path.getsize(p))
print()
print('=== Git 仓库检查 ===')
gitdir = r'c:\Users\Admin1\Documents\FastViewCloudService\.git'
print('工作区 .git 存在:', os.path.isdir(gitdir))
print()
print('=== 根目录文件 ===')
for f in sorted(os.listdir(r'c:\Users\Admin1\Documents\FastViewCloudService')):
    if os.path.isfile(os.path.join(r'c:\Users\Admin1\Documents\FastViewCloudService', f)):
        print(f)
