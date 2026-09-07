# -*- coding: utf-8 -*-
"""全库最终扫描：工作区+桌面版全部HTML断链 & 残留旧文件名引用"""
import os, re, glob

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

OLD_NAMES = ['econ-thought.html', 'art-aesthetics.html', 'eastern-thought.html', 'edu-lineage.html']


def scan_tree(root, label):
    htmls = glob.glob(os.path.join(root, '**', '*.html'), recursive=True)
    total_links = 0
    broken = []
    old_refs = []
    for hf in htmls:
        try:
            c = open(hf, encoding='utf-8').read()
        except Exception:
            continue
        base = os.path.dirname(hf)
        for m in re.finditer(r'href="([^"#]+?\.html)"', c):
            href = m.group(1)
            if href.startswith(('http://', 'https://', 'mailto:')):
                continue
            total_links += 1
            full = os.path.normpath(os.path.join(base, href))
            if not os.path.exists(full):
                broken.append((os.path.relpath(hf, root), href))
        for old in OLD_NAMES:
            if old in c:
                old_refs.append((os.path.relpath(hf, root), old))
    print('==== {} ===='.format(label))
    print('  卷内HTML文件: {} 个, 内链总数: {} 个'.format(len(htmls), total_links))
    print('  断链: {} 个'.format(len(broken)))
    for rel, href in broken[:20]:
        print('    BROKEN {} -> {}'.format(rel, href))
    if len(broken) > 20:
        print('    ... 其余省略')
    print('  旧文件名引用: {} 处'.format(len(old_refs)))
    for rel, old in old_refs[:20]:
        print('    OLDREF {} -> {}'.format(rel, old))
    print()
    return broken, old_refs


b1, o1 = scan_tree(ws, '工作区 FastViewCloudService')
b2, o2 = scan_tree(dt, '桌面版 Trae资料库')
