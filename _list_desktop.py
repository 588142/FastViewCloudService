# -*- coding: utf-8 -*-
"""盘点桌面版每个目录的中文HTML文件，生成权威映射"""
import os

dt = r'c:\Users\Admin1\Desktop\Trae资料库'

print('=== 桌面版各目录文件盘点 ===')
for d in sorted(os.listdir(dt)):
    dp = os.path.join(dt, d)
    if not os.path.isdir(dp):
        continue
    htmls = [f for f in os.listdir(dp) if f.endswith('.html')]
    print('%-28s -> %s' % (d, htmls))