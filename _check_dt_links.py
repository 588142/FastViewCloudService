# -*- coding: utf-8 -*-
"""检查桌面版 index.html / 主题索引.html 的原始链接路径形态"""
import os, re

dt = r'c:\Users\Admin1\Desktop\Trae资料库'
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

# 桌面版实际目录名
dt_dirs = set(os.listdir(dt))

for fname in ['index.html', '主题索引.html']:
    fp = os.path.join(dt, '思想图谱系列', fname)
    c = open(fp, encoding='utf-8').read()
    print('==== 桌面版 {} ===='.format(fname))
    links = re.findall(r'href="\.\./([^"]*)"', c)
    # 英文目录名模式（工作区命名风格）
    en_pat = re.compile(r'^[a-z][a-z0-9-]*/')
    english = [l for l in links if en_pat.match(l)]
    chinese = [l for l in links if not en_pat.match(l)]
    print('  共{}个链接，英文目录{}个，中文目录{}个'.format(len(links), len(english), len(chinese)))
    print('  英文目录链接（原始形态）:')
    for l in sorted(set(english)):
        # 该链接对应桌面目录是否存在？
        dirname = l.split('/')[0]
        exists = dirname in dt_dirs
        full = os.path.normpath(os.path.join(dt, '思想图谱系列', '..', l))
        fexists = os.path.exists(full)
        flag = 'OK' if fexists else 'BROKEN!!'
        print('    [{}] {}'.format(flag, l))
    print()
