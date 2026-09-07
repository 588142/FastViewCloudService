# -*- coding: utf-8 -*-
import os, re, shutil
ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

vol_dir = 'economics-lineage'
html_file = 'economics-lineage.html'
frag_name = '_appendix_economics-lineage.html'
toc_anchor = '<li><a href="#formulas">第七章 · 总结 · 常用经济公式速查</a></li>'
new_meta = '<p class="meta">作者：詹家杨 · 2026-09-06 · 6 张思维导图 · 2 张对照表 · 20+ 常用经济公式 · 30+ 人物语录 · 11 个本科升级附录（术语表 · 供需3D曲面 · 生产函数 · 习题集 · 文献选读）</p>'
toc_append = '''
      <li style="margin-top:0.9rem;font-weight:700;color:var(--accent2);font-size:0.8rem;">★ 本科生升级附录</li>
      <li><a href="#appendix-a">附录一 · 升级导览与教材对标</a></li>
      <li><a href="#appendix-b">附录二 · 精确定义与术语表</a></li>
      <li><a href="#appendix-c">附录三 · 形式系统与核心模型</a></li>
      <li><a href="#appendix-d">附录四 · 推演方法与证明</a></li>
      <li><a href="#appendix-e">附录五 · 核心模型与图表</a></li>
      <li><a href="#appendix-f">附录六 · 高阶理论与前沿</a></li>
      <li><a href="#appendix-g">附录七 · 方法训练与实操指南</a></li>
      <li><a href="#appendix-h">附录八 · 经典习题集</a></li>
      <li><a href="#appendix-i">附录九 · 一手文献选读</a></li>
      <li><a href="#appendix-j">附录十 · 关键争论</a></li>
      <li><a href="#appendix-k">附录十一 · 延伸阅读与课程</a></li>'''

html_path = os.path.join(ws, vol_dir, html_file)
frag_path = os.path.join(ws, frag_name)

# 先从备份恢复
bak = html_path + '.bak2'
if os.path.exists(bak):
    shutil.copy2(bak, html_path)
    print('已从备份恢复')

c = open(html_path, encoding='utf-8').read()
frag = open(frag_path, encoding='utf-8').read().strip()

# 1) 插入附录
pos = c.index('</main>') + len('</main>')
if 'appendix-a' in c:
    # 删除旧的附录内容
    old_appendix = c[c.index('id="appendix-a"'):]
    # 找到old_appendix的结束位置
    next_section_pos = c.index('<section', c.index('</main>'))
    c = c[:c.index('id="appendix-a"')] + c[c.index('</main>') + len('</main>'):].split('<section')[0]
    pos = c.index('</main>') + len('</main>')
    c = c[:pos] + '\n\n' + frag + '\n' + c[pos:]
    print('附录已替换')
else:
    c = c[:pos] + '\n\n' + frag + '\n' + c[pos:]
    print('附录已插入')

# 2) TOC
if toc_anchor in c:
    c = c.replace(toc_anchor, toc_anchor + '\n' + toc_append, 1)
    print('侧边目录已更新')
else:
    all_links = re.findall(r'<li><a href="#[^"]*">[^<]*</a></li>', c)
    if all_links:
        last = all_links[-1]
        c = c.replace(last, last + '\n' + toc_append, 1)
        print(f'  fallback 使用: {last[:40]}')

# 3) meta
old_meta = re.search(r'<p class="meta">[^<]*</p>', c)
if old_meta:
    c = c.replace(old_meta.group(0), new_meta, 1)
    print('meta已更新')

open(html_path, 'w', encoding='utf-8').write(c)
print(f'写入完成: {len(c)} 字节')