# -*- coding: utf-8 -*-
"""对比工作区与桌面版 index.html 内容"""
import re

ws = r'c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列\index.html'
dt = r'c:\Users\Admin1\Desktop\Trae资料库\思想图谱系列\index.html'

for label, fp in [('工作区', ws), ('桌面版', dt)]:
    c = open(fp, encoding='utf-8').read()
    title = re.search(r'<title>([^<]*)</title>', c)
    h1 = re.search(r'<h1[^>]*>([^<]*)</h1>', c)
    en_links = re.findall(r'href="\.\./([a-z][a-z-]+)/', c)
    cn_links = re.findall(r'href="\.\./([\u4e00-\u9fff][^/"]*)/', c)
    print('=== %s ===' % label)
    print('  title:', title.group(1).strip() if title else '无')
    print('  h1:', h1.group(1).strip() if h1 else '无')
    print('  英文目录链接: %d' % len(en_links))
    print('  中文目录链接: %d' % len(cn_links))
    print('  英文目录示例:', sorted(set(en_links))[:8])
    print('  含★高阶:', '高阶内容' in c)
    print('  含硕士:', '硕士' in c)
    print('  含博士:', '博士' in c)
    print()