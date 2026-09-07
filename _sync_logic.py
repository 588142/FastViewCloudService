# -*- coding: utf-8 -*-
"""同步 logic-lineage 到桌面版并验证"""
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

src = os.path.join(ws, 'logic-lineage', 'logic-lineage.html')
c = open(src, encoding='utf-8').read()

en_to_cn = {
    'truth-dimensions': '真理的多维图景', 'marxism-lineage': '马克思主义谱系',
    'economics-lineage': '经济思想谱系', 'econ-part2-lineage': '经济思想谱系下篇',
    'psych-lineage': '心理学思想谱系', 'math-lineage': '数学思想谱系',
    'logic-lineage': '逻辑与论证思想谱系', 'philosophy-lineage': '西方哲学思想谱系',
    'science-lineage': '科学思想谱系', 'social-thought': '社会思想谱系',
    'history-lineage': '历史思想谱系', 'ethics-lineage': '伦理与道德思想谱系',
    'literature-lineage': '文学与语言思想谱系', 'rhetoric-lineage': '修辞与演说思想谱系',
    'education-lineage': '教育思想谱系', 'life-science-lineage': '生命科学思想谱系',
    'tech-ai-lineage': '科技与人工智能思想谱系', 'politics-lineage': '政治学通论',
    'liberalism-lineage': '自由主义谱系', 'isms-glossary': '政治基础概念1',
    'law-lineage': '法哲学思想谱系', 'eastern-thought-lineage': '东方思想谱系',
    'art-aesthetics-lineage': '艺术与美学思想谱系', 'anthropology-lineage': '人类学思想谱系',
    'media-lineage': '传播与媒介思想谱系', 'military-lineage': '军事与战略思想谱系',
    'ir-lineage': '国际关系思想谱系', 'geo-lineage': '地理与环境思想谱系',
    'religion-lineage': '宗教学与神话', 'astronomy-lineage': '天文学与宇宙学',
    'physics-lineage': '物理学', 'chemistry-lineage': '化学',
    'cs-lineage': '计算机科学', 'linguistics-lineage': '语言学',
    'medicine-lineage': '医学与健康', '思想图谱系列': '思想图谱系列',
    'series-overview': 'series-overview',
}
for en, cn in en_to_cn.items():
    c = c.replace('../' + en + '/', '../' + cn + '/')

dd = os.path.join(dt, '逻辑与论证思想谱系')
for fname in ['logic-lineage.html', '逻辑与论证思想谱系.html']:
    df = os.path.join(dd, fname)
    if os.path.exists(df):
        bak = df + '.bak2'
        if not os.path.exists(bak):
            shutil.copy2(df, bak)
    open(df, 'w', encoding='utf-8').write(c)
    print('已同步:', fname)

print()
print('=== 桌面版验证 ===')
for fname in ['logic-lineage.html', '逻辑与论证思想谱系.html']:
    cc = open(os.path.join(dd, fname), encoding='utf-8').read()
    cc2 = re.sub(r'<script[\s\S]*?</script>', '', cc, flags=re.I)
    cc2 = re.sub(r'<style[\s\S]*?</style>', '', cc2, flags=re.I)
    do = len(re.findall(r'<div[\s>]', cc2))
    dc = cc2.count('</div>')
    nm = (cc.count('<main'), cc.count('</main>'))
    nf = cc.count('<footer')
    nshell = cc.count('class="shell"')
    broken = [l for l in re.findall(r'href="\.\./([^"]*)"', cc)
              if not os.path.exists(os.path.normpath(os.path.join(dd, '..', l)))]
    print('{}: div{}/{} main{}/{} footer{} shell{} 断链{}'.format(
        fname, do, dc, nm[0], nm[1], nf, nshell, len(broken)))
