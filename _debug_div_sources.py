# -*- coding: utf-8 -*-
"""检查marxism-lineage：注释/SVG中的div干扰 + 真实的div平衡"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 1. 统计注释里的 </div>
comments = re.findall(r'<!--.*?-->', c, re.DOTALL)
div_in_comment = [cm for cm in comments if '</div>' in cm or '<div' in cm]
print(f'注释总数: {len(comments)}, 含div的注释: {len(div_in_comment)}')
for cm in div_in_comment[:5]:
    print(f'  注释片段: {cm[:100]}')

# 2. 统计SVG里的div（应该没有）
svgs = re.findall(r'<svg.*?</svg>', c, re.DOTALL)
div_in_svg = [s for s in svgs if '<div' in s or '</div>' in s]
print(f'SVG总数: {len(svgs)}, 含div的SVG: {len(div_in_svg)}')

# 3. 字符串里JS的</div>？
scripts = re.findall(r'<script.*?</script>', c, re.DOTALL)
div_in_js = [s for s in scripts if '</div>' in s]
print(f'script总数: {len(scripts)}, JS里含</div>的: {len(div_in_js)}')

# 4. 干净文本（去注释+script+style）里的div平衡
c_clean = re.sub(r'<!--.*?-->', '', c, flags=re.DOTALL)
c_clean = re.sub(r'<script.*?</script>', '', c_clean, flags=re.DOTALL)
c_clean = re.sub(r'<style.*?</style>', '', c_clean, flags=re.DOTALL)
# 去掉SVG块（foreign content按XML规则，但div不会出现在SVG里）
c_clean2 = re.sub(r'<svg.*?</svg>', '', c_clean, flags=re.DOTALL)

d_open = len(re.findall(r'<div(?:\s[^>]*)?>', c_clean2))
d_close = len(re.findall(r'</div>', c_clean2))
print(f'干净文本: <div>={d_open} </div>={d_close} 差={d_open-d_close}')
