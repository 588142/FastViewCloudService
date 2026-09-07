# -*- coding: utf-8 -*-
import re
fp = r'c:\Users\Admin1\Documents\FastViewCloudService\economics-lineage\economics-lineage.html'
c = open(fp, encoding='utf-8').read()
three_scripts = list(re.finditer(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c))
print(f'Three.js引用数: {len(three_scripts)}')
for i, m in enumerate(three_scripts):
    print(f'  #{i}: ...{c[m.start():m.end()][:80]}...')
if len(three_scripts) > 1:
    for m in reversed(three_scripts[1:]):
        c = c[:m.start()] + '<!-- three.min.js 已在上方加载 -->' + c[m.end():]
    open(fp, 'w', encoding='utf-8').write(c)
    # 验证
    c2 = open(fp, encoding='utf-8').read()
    final_count = len(re.findall(r'<script[^>]*src="[^"]*three\.min\.js[^"]*"', c2))
    print(f'修复后: {final_count}')
else:
    print('无需修复')