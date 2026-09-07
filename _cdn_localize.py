# -*- coding: utf-8 -*-
"""CDN 本地化：将 all html 中的 three.js/chart.js/OrbitControls/mermaid CDN 引用替换为本地 _shared/js。"""
import os, shutil, sys

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'
DL = os.path.join(ROOT, '_dl')

REPLACEMENTS = [
    ('https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js', './_shared/js/chart.umd.min.js'),
    ('https://cdn.jsdelivr.net/npm/chart.js@4', './_shared/js/chart.umd.min.js'),
    ('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', './_shared/js/three.min.js'),
    ('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js', './_shared/js/OrbitControls.js'),
    ('https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js', './_shared/js/mermaid.min.js'),
]

LIBS = {
    'three':  ('three.min.js', DL),
    'chart':  ('chart.umd.min.js', DL),
    'orbit':  ('OrbitControls.js', DL),
    'mermaid': ('mermaid.min.js', None),  # 源从已有卷复制
}

def find_mermaid_src():
    for dp, dn, fn in os.walk(ROOT):
        if '_dl' in dp or '__pycache__' in dp:
            continue
        for f in fn:
            if f == 'mermaid.min.js':
                return os.path.join(dp, f)
    return None

def main():
    if not os.path.isdir(DL):
        print('ERROR: _dl 不存在'); sys.exit(1)
    mermaid_src = find_mermaid_src()
    if not mermaid_src:
        print('ERROR: 未找到 mermaid.min.js 源'); sys.exit(1)

    targets = []   # (file_path, libs_set)
    for dp, dn, fn in os.walk(ROOT):
        if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            c = open(p, encoding='utf-8').read()
            libs = set()
            if 'cdnjs.cloudflare.com/ajax/libs/three.js/r128' in c: libs.add('three')
            if 'cdn.jsdelivr.net/npm/chart.js' in c: libs.add('chart')
            if 'examples/js/controls/OrbitControls.js' in c: libs.add('orbit')
            if 'cdn.jsdelivr.net/npm/mermaid@10' in c: libs.add('mermaid')
            if libs:
                targets.append((p, libs))

    modified, copied = [], []
    for p, libs in targets:
        # 定位该文件的 _shared/js 目录：优先同级目录下的 _shared，否则根目录级 _shared
        d = os.path.dirname(p)
        vol_shared = os.path.join(d, '_shared', 'js')
        root_shared = os.path.join(ROOT, '_shared', 'js')
        # 文件在卷目录内（目录名含 _shared 或目录为卷名）→ 用卷内 _shared；根目录散件 → 根 _shared
        use = vol_shared if os.path.isdir(os.path.join(d, '_shared')) else root_shared
        os.makedirs(use, exist_ok=True)
        for lib in libs:
            name, srcdir = LIBS[lib]
            src = os.path.join(srcdir, name) if srcdir else mermaid_src
            dst = os.path.join(use, name)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                copied.append(dst)
        # 替换引用
        c = open(p, encoding='utf-8').read()
        orig = c
        for old, new in REPLACEMENTS:
            if old in c:
                c = c.replace(old, new)
        if c != orig:
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(c)
            modified.append(p)

    print(f'=== 修改文件 {len(modified)} 个 ===')
    for m in modified:
        print('  M:', os.path.relpath(m, ROOT))
    print(f'=== 复制库文件 {len(copied)} 个 ===')
    for c in sorted(set(copied)):
        print('  C:', os.path.relpath(c, ROOT))

    # 复查：不应再有 CDN 引用
    left = []
    for dp, dn, fn in os.walk(ROOT):
        if '_dl' in dp or '__pycache__' in dp or '.git' in dp:
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            c = open(p, encoding='utf-8').read()
            for m in __import__('re').finditer(r'src="(https?://[^"]+)"', c):
                left.append((os.path.relpath(p, ROOT), m.group(1)))
    print(f'=== 剩余外部引用 {len(left)} 个 ===')
    for l in left:
        print('  !', l[0], '->', l[1])

    # 本地引用存在性检查
    print('=== 本地引用存在性 ===')
    bad = 0
    for p, libs in targets:
        c = open(p, encoding='utf-8').read()
        for m in __import__('re').finditer(r'src="(\./_shared/js/[^"]+)"', c):
            rel = m.group(1)
            d = os.path.dirname(p)
            target = os.path.normpath(os.path.join(d, rel))
            if not os.path.exists(target):
                print('  MISSING:', os.path.relpath(p, ROOT), '->', rel)
                bad += 1
    print(f'  缺失引用: {bad} 个')

if __name__ == '__main__':
    main()
