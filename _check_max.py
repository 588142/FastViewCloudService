# -*- coding: utf-8 -*-
"""查看块3(masters CSS)中 :root 的 --max 及 body/shell 完整定义"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

styles = [(m.start(), m.group(1)) for m in re.finditer(r'<style[^>]*>([\s\S]*?)</style>', c, re.I)]
for bi, (pos, css) in enumerate(styles):
    line = c[:pos].count('\n') + 1
    m = re.search(r':root\s*\{([^}]*)\}', css)
    mx = re.search(r'--max\s*:\s*([^;]+);', m.group(1)) if m else None
    print('块{} @行{}  --max={}'.format(bi + 1, line, mx.group(1).strip() if mx else 'N/A'))

# 块3中 body 和 .shell 完整定义
css3 = styles[2][1]
for pat in [r'body\s*\{[^}]*\}', r'\.shell\s*\{[^}]*\}', r'main\s*\{[^}]*\}', r'\.page\s*\{[^}]*\}', r'article\s*\{[^}]*\}', r'\.sec\s*\{[^}]*\}']:
    for m in re.finditer(pat, css3):
        print('[块3]', m.group(0).replace('\n', ' ')[:200])
