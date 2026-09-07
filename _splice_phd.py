# -*- coding: utf-8 -*-
"""博士水平进阶模块拼接脚本。用法: python _splice_phd.py <volume_dir> <fragment_path>"""
import os, re, sys, shutil
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vol_dir = sys.argv[1]
frag_path = sys.argv[2]

html_path = os.path.join(ws, vol_dir, f'{vol_dir}.html')
if not os.path.exists(html_path):
    import glob
    files = glob.glob(os.path.join(ws, vol_dir, '*.html'))
    html_path = files[0] if files else exit(f'找不到 {vol_dir} 下的HTML')

frag = open(frag_path, encoding='utf-8').read().strip()
c = open(html_path, encoding='utf-8').read()

# 在硕士模块之后插入博士模块（找 masters-m8 的完整 </section>）
if 'id="masters-m8"' in c:
    m8_start = c.index('id="masters-m8"')
    # 找到该 section 真正的结束标签：数到正确层级的 </section>
    depth = 1  # 已在 section 内部
    i = m8_start
    while i < len(c):
        open_pos = c.find('<section', i)
        close_pos = c.find('</section>', i)
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            i = open_pos + 8
        elif close_pos != -1:
            depth -= 1
            i = close_pos + 10
            if depth == 0:
                m8_end = i
                break
        else:
            break
    if 'id="phd-prologue"' in c:
        print('博士模块已存在')
    else:
        c = c[:m8_end] + '\n\n' + frag + '\n' + c[m8_end:]
        print('博士模块已插入')
else:
    if 'id="appendix-k"' in c:
        ak_start = c.index('id="appendix-k"')
        depth = 1
        i = ak_start
        while i < len(c):
            open_pos = c.find('<section', i)
            close_pos = c.find('</section>', i)
            if open_pos != -1 and open_pos < close_pos:
                depth += 1; i = open_pos + 8
            elif close_pos != -1:
                depth -= 1; i = close_pos + 10
                if depth == 0: ak_end = i; break
            else: break
        c = c[:ak_end] + '\n\n' + frag + '\n' + c[ak_end:]
        print('博士模块已插入（无硕士模块）')
    else:
        exit('找不到插入点')

# 更新侧边目录
toc_add = '''
      <li style="margin-top:0.9rem;font-weight:700;color:var(--accent2);font-size:0.8rem;">▸ 博士水平进阶</li>
      <li><a href="#phd-prologue">博导 · 导览</a></li>
      <li><a href="#phd-d1">D1 · 核心公理与定义</a></li>
      <li><a href="#phd-d2">D2 · 基本定律与原理</a></li>
      <li><a href="#phd-d3">D3 · 核心定理</a></li>
      <li><a href="#phd-d4">D4 · 定理证明详解</a></li>
      <li><a href="#phd-d5">D5 · 形式化体系</a></li>
      <li><a href="#phd-d6">D6 · 前沿定理与未解问题</a></li>
      <li><a href="#phd-d7">D7 · 研究前沿</a></li>'''

# 在硕士TOC之后追加
masters_toc = '<li><a href="#masters-m8">M8 · 研究实践与论文</a></li>'
if masters_toc in c:
    c = c.replace(masters_toc, masters_toc + '\n' + toc_add, 1)
    print('TOC已更新')
else:
    # fallback: 找最后一个硕士TOC链接
    mm = re.findall(r'<li><a href="#masters-m[1-8]">[^<]*</a></li>', c)
    if mm:
        c = c.replace(mm[-1], mm[-1] + '\n' + toc_add, 1)
        print('TOC fallback 已更新')

# 更新meta
c = re.sub(r'<p class="meta">[^<]*</p>',
           lambda m: m.group(0).replace('硕士', '博士').replace('硕士', '博士') if '博士' not in m.group(0) else m.group(0),
           c, count=1)
if '博士' not in [m.group(0) for m in re.finditer(r'<p class="meta">[^<]*</p>', c)]:
    c = re.sub(r'<p class="meta">[^<]*</p>',
               lambda m: m.group(0).replace('</p>', ' · 7 个博士进阶模块</p>'),
               c, count=1)

bak = html_path + '.bak4'
if not os.path.exists(bak):
    shutil.copy2(html_path, bak)
open(html_path, 'w', encoding='utf-8').write(c)
print(f'写入完成: {len(c)} bytes')