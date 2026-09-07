# -*- coding: utf-8 -*-
"""同步liberalism-lineage到桌面版"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

src = os.path.join(ws, 'liberalism-lineage', 'liberalism-lineage.html')
c = open(src, encoding='utf-8').read()

en_to_cn = {
    'philosophy-lineage': '西方哲学思想谱系',
    'economics-lineage': '经济思想谱系',
    'politics-lineage': '政治学通论',
    'marxism-lineage': '马克思主义谱系',
    'history-lineage': '历史思想谱系',
    'law-lineage': '法哲学思想谱系',
    'eastern-thought-lineage': '东方思想谱系',
    '思想图谱系列': '思想图谱系列',
}
for en, cn in en_to_cn.items():
    c = c.replace('../' + en + '/', '../' + cn + '/')

dd = os.path.join(dt, '自由主义谱系')
for fname in ['liberalism-lineage.html', '自由主义谱系.html']:
    df = os.path.join(dd, fname)
    if os.path.exists(df):
        bak = df + '.bak'
        if not os.path.exists(bak):
            shutil.copy2(df, bak)
    open(df, 'w', encoding='utf-8').write(c)
    print('已同步:', fname)

for fname in ['liberalism-lineage.html', '自由主义谱系.html']:
    cc = open(os.path.join(dd, fname), encoding='utf-8').read()
    broken = [l for l in re.findall(r'href="\.\./([^"]*)"', cc)
              if not os.path.exists(os.path.normpath(os.path.join(dd, '..', l)))]
    do = len(re.findall(r'<div[\s>]', cc))
    dc = cc.count('</div>')
    print('{}: 断链{} div {}/{}'.format(fname, len(broken), do, dc))
