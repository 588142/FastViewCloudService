# -*- coding: utf-8 -*-
"""定位重复 masthead / style 块位置"""
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
c = open(fp, encoding='utf-8').read()

for pat, name in [(r'class="masthead"', 'masthead'), (r'<style', '<style>'), (r'</style>', '</style>'),
                  (r'class="series-bar"', 'series-bar'), (r'<article', '<article'), (r'</article>', '</article>'),
                  (r'<header', '<header'), (r'</header>', '</header>'), (r'<main', '<main'), (r'</main>', '</main>')]:
    poss = [c[:m.start()].count('\n') + 1 for m in re.finditer(pat, c)]
    print('{:14s} {} 次 @行 {}'.format(name, len(poss), poss))
