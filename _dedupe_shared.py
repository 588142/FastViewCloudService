# -*- coding: utf-8 -*-
"""P1 资源去重：卷内 _shared 收敛为站级共享（中文站 思想图谱系列\_shared，英文站根 _shared），删除卷内 _shared。"""
import os, re, shutil

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'
CN = os.path.join(ROOT, '思想图谱系列')
ROOT_SHARED = os.path.join(ROOT, '_shared')
CN_SHARED = os.path.join(CN, '_shared')

JS_FILES = ['mermaid.min.js', 'three.min.js', 'chart.umd.min.js', 'OrbitControls.js', 'echarts.min.js']
FONT_FILES = [
    'Lora-Regular.ttf', 'Lora-Bold.ttf', 'Lora-Italic.ttf',
    'WorkSans-Regular.ttf', 'WorkSans-Bold.ttf', 'DMMono-Regular.ttf',
    'CrimsonPro-Regular.ttf', 'CrimsonPro-Bold.ttf', 'CrimsonPro-Italic.ttf',
    'InstrumentSans-Regular.ttf', 'InstrumentSans-Bold.ttf', 'InstrumentSans-Italic.ttf',
    'JetBrainsMono-Regular.ttf', 'JetBrainsMono-Bold.ttf',
]

def find_src(name):
    for dp, dn, fn in os.walk(ROOT):
        if '_dl' in dp or '__pycache__' in dp or '.git' in dp or '_shared' not in dp:
            continue
        if name in fn:
            return os.path.join(dp, name)
    return None

def ensure(shared_js, shared_fonts):
    os.makedirs(shared_js, exist_ok=True)
    os.makedirs(shared_fonts, exist_ok=True)
    for n in JS_FILES:
        dst = os.path.join(shared_js, n)
        if not os.path.exists(dst):
            src = find_src(n)
            if not src:
                print('!!! 找不到源文件:', n); continue
            shutil.copy2(src, dst)
    for n in FONT_FILES:
        dst = os.path.join(shared_fonts, n)
        if not os.path.exists(dst):
            src = find_src(n)
            if not src:
                print('!!! 找不到源文件:', n); continue
            shutil.copy2(src, dst)

# 1. 建立两个站级共享目录
ensure(os.path.join(ROOT_SHARED, 'js'), os.path.join(ROOT_SHARED, 'fonts'))
ensure(os.path.join(CN_SHARED, 'js'), os.path.join(CN_SHARED, 'fonts'))
print('站级共享目录建立完成')

# 2. 修改引用
cn_vol_re = re.compile(r'^思想图谱系列\\[^\\]+\\')
en_vol_re = re.compile(r'^[^\\]+\\[^\\]+\.html$')  # 根下 卷\卷.html（非 _ 前缀）
modified = []
for dp, dn, fn in os.walk(ROOT):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        c = open(p, encoding='utf-8').read()
        orig = c
        if rel.startswith('思想图谱系列\\') and rel.count('\\') >= 2:
            # 中文站卷内：./_shared/ -> ../_shared/
            c = c.replace('./_shared/', '../_shared/')
        elif rel.startswith('思想图谱系列\\'):
            # 中文站根级：寄生字体引用收敛
            c = re.sub(r'\.\./[^/"\'()]+/_shared/fonts/', './_shared/fonts/', c)
            c = re.sub(r'\./[^/"\'()]+/_shared/fonts/', './_shared/fonts/', c)
        elif rel.count('\\') == 1 and not rel.startswith('_') and not rel.startswith('思想图谱系列'):
            # 英文站卷内：./_shared/ -> ../_shared/
            c = c.replace('./_shared/', '../_shared/')
        elif rel.startswith('_') and rel.count('\\') == 0:
            # 根散件：寄生字体引用收敛
            c = re.sub(r'\./[^/"\'()]+/_shared/fonts/', './_shared/fonts/', c)
        if c != orig:
            open(p, 'w', encoding='utf-8').write(c)
            modified.append(rel)
print(f'引用修改 {len(modified)} 个文件')

# 3. 删除所有卷内 _shared 目录
deleted = []
for dp, dn, fn in os.walk(ROOT, topdown=False):
    if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
        continue
    for d in dn:
        if d == '_shared':
            full = os.path.join(dp, d)
            if full in (ROOT_SHARED, CN_SHARED):
                continue
            size = sum(os.path.getsize(os.path.join(full, x)) for x in os.listdir(full) if os.path.isfile(os.path.join(full, x)))
            shutil.rmtree(full)
            deleted.append((os.path.relpath(full, ROOT), size))
print(f'删除卷内 _shared {len(deleted)} 个，释放 {sum(s for _, s in deleted)/1048576:.1f} MB')
