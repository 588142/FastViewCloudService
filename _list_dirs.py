# -*- coding: utf-8 -*-
import os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

ws_dirs = sorted([d for d in os.listdir(ws) if os.path.isdir(os.path.join(ws, d)) and not d.startswith('_') and not d.startswith('.')])
dt_dirs = sorted([d for d in os.listdir(dt) if os.path.isdir(os.path.join(dt, d)) and not d.startswith('_')])

print('=== 工作区目录 ===')
print(ws_dirs)
print(f'\n=== 桌面版目录 ({len(dt_dirs)}) ===')
print(dt_dirs)
