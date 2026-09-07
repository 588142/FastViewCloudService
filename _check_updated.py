# -*- coding: utf-8 -*-
"""检查工作区各卷是否今天(09-07)有更新，找出桌面版可能落后于工作区的文件"""
import os, datetime

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

# 今天日期
today = '2026-09-07'

print('=== 工作区各卷 HTML 修改时间（今天更新者标记） ===')
vols = {}
for d in os.listdir(ws):
    dp = os.path.join(ws, d)
    if not os.path.isdir(dp) or d.startswith(('.', '_')):
        continue
    for f in os.listdir(dp):
        if f.endswith('.html') and not f.endswith('.bak'):
            fp = os.path.join(dp, f)
            mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
            ds = mt.strftime('%Y-%m-%d %H:%M')
            key = d + '/' + f
            vols[key] = (ds, os.path.getsize(fp)//1024)
            if ds.startswith(today):
                print('  [今天更新] %-45s %5d KB  %s' % (key, vols[key][1], ds))

print()
print('=== 时间戳分布统计 ===')
from collections import Counter
c = Counter(v.split()[0] for v, _ in vols.values())
for day, cnt in sorted(c.items()):
    print('  %s: %d 个文件' % (day, cnt))

print()
print('=== 全部卷文件（按时间倒序前20） ===')
sorted_vols = sorted(vols.items(), key=lambda x: x[1][0], reverse=True)
for key, (ds, size) in sorted_vols[:20]:
    print('  %-45s %5d KB  %s' % (key, size, ds))