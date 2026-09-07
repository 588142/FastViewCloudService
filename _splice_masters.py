# -*- coding: utf-8 -*-
"""
硕士水平进阶模块拼接脚本。
用法: python _splice_masters.py <volume_dir> <fragment_path> <toc_anchor_text>
"""
import os, re, sys, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vol_dir = sys.argv[1]
frag_path = sys.argv[2]
toc_anchor = sys.argv[3]

html_path = os.path.join(ws, vol_dir, f'{vol_dir}.html')
if not os.path.exists(html_path):
    html_path = os.path.join(ws, vol_dir, f'{vol_dir.replace("-","")}.html')
if not os.path.exists(html_path):
    import glob
    files = glob.glob(os.path.join(ws, vol_dir, '*.html'))
    html_path = files[0] if files else exit(f'找不到 {vol_dir} 下的HTML')

print(f'目标: {html_path}')
frag = open(frag_path, encoding='utf-8').read().strip()
c = open(html_path, encoding='utf-8').read()

# 在最后一个 appendix 之后插入硕士模块
# 找 </section> 之后紧跟 appendix-k 的
if 'id="appendix-k"' in c:
    # 在 appendix-k 的 </section> 之后插入
    ak_end = c.index('</section>', c.index('id="appendix-k"'))
    ak_end = c.index('</section>', ak_end + 10) + len('</section>')
    
    if 'id="masters-prologue"' in c:
        print('硕士模块已存在，跳过')
    else:
        c = c[:ak_end] + '\n\n' + frag + '\n' + c[ak_end:]
        print('硕士模块已插入')
else:
    print('!! 未找到 appendix-k')

# 更新侧边目录：在附录十一之后追加硕士模块入口
toc_add = '''
      <li style="margin-top:0.9rem;font-weight:700;color:var(--accent2);font-size:0.8rem;">▸ 硕士水平进阶</li>
      <li><a href="#masters-prologue">进阶级 · 概览与路线</a></li>
      <li><a href="#masters-m1">M1 · 高阶理论框架</a></li>
      <li><a href="#masters-m2">M2 · 形式化与数学基础</a></li>
      <li><a href="#masters-m3">M3 · 核心论文精读</a></li>
      <li><a href="#masters-m4">M4 · 研究方法论</a></li>
      <li><a href="#masters-m5">M5 · 前沿议题</a></li>
      <li><a href="#masters-m6">M6 · 跨学科交叉</a></li>
      <li><a href="#masters-m7">M7 · 批判性分析</a></li>
      <li><a href="#masters-m8">M8 · 研究实践与论文</a></li>'''

if toc_anchor in c:
    c = c.replace(toc_anchor, toc_anchor + '\n' + toc_add, 1)
    print(f'TOC已更新')
else:
    all_links = re.findall(r'<li><a href="#appendix-k">[^<]*</a></li>', c)
    if all_links:
        c = c.replace(all_links[-1], all_links[-1] + '\n' + toc_add, 1)
        print('TOC fallback 已更新')
    else:
        print('!! 无法更新TOC')

# 更新meta行
old_meta = re.search(r'<p class="meta">[^<]*</p>', c)
if old_meta:
    new_meta = old_meta.group(0).replace('本科', '本科+硕士').replace('附录', '附录+硕士模块')
    if '硕士' not in new_meta:
        new_meta = new_meta.replace('</p>', ' · 8 个硕士进阶模块</p>')
    c = c.replace(old_meta.group(0), new_meta, 1)
    print('meta已更新')

bak = html_path + '.bak3'
if not os.path.exists(bak):
    shutil.copy2(html_path, bak)
open(html_path, 'w', encoding='utf-8').write(c)
print(f'写入完成: {len(c)} bytes')