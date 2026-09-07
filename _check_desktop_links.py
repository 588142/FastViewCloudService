# -*- coding: utf-8 -*-
import re
c1 = open(r'c:\Users\Admin1\Desktop\Trae资料库\马克思主义谱系\马克思主义谱系.html', encoding='utf-8').read()
links = re.findall(r'href="(\.\./[^"]*)"', c1)
print('中文名文件 跨卷链接:')
for l in links[:6]:
    print(f'  {l}')

c2 = open(r'c:\Users\Admin1\Desktop\Trae资料库\马克思主义谱系\marxism-lineage.html', encoding='utf-8').read()
links2 = re.findall(r'href="(\.\./[^"]*)"', c2)
print('英文名文件 跨卷链接:')
for l in links2[:6]:
    print(f'  {l}')
