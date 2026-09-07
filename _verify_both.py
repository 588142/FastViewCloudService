# -*- coding: utf-8 -*-
"""验证工作区和桌面版的结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
dt = r'c:\Users\Admin1\Desktop\Trae资料库\逻辑与论证思想谱系\逻辑与论证思想谱系.html'

for label, fp in [('工作区', ws), ('桌面版', dt)]:
    if not os.path.exists(fp):
        print('%s: 文件不存在' % label)
        continue
    c = open(fp, encoding='utf-8').read()
    print('=== %s (%dKB) ===' % (label, len(c)//1024))
    print('  shell容器:', c.count('class="shell"'))
    print('  masthead:', c.count('class="masthead"'))
    print('  main:', c.count('<main'), '/', c.count('</main>'))
    print('  footer:', c.count('<footer'))
    body_pad = re.search(r'body\s*\{[^}]*padding[^}]*\}', c)
    print('  body padding:', body_pad.group(0)[:60] if body_pad else '无')
    shell_max = re.search(r'\.shell\s*\{[^}]*\}', c)
    print('  .shell定义:', shell_max.group(0).replace('\n',' ')[:80] if shell_max else '无')
    main_secs = len(re.findall(r'<section', c))
    print('  section总数:', main_secs)
    # 断链检查
    base = os.path.dirname(fp)
    links = re.findall(r'href="([^"#]+?\.html)"', c)
    broken = [l for l in links if not l.startswith('http') and not os.path.exists(os.path.normpath(os.path.join(base, l)))]
    print('  断链:', len(broken), broken[:5] if broken else '无')
    print()