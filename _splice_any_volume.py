# -*- coding: utf-8 -*-
"""
通用拼接脚本：将附录片段插入指定卷宗，更新侧边目录和meta行。
用法: python _splice_any_volume.py <volume_dir> <appendix_fragment_path> <meta_line> <toc_anchor_text> <toc_append_html>
"""
import os, re, sys

fp = r'c:\Users\Admin1\Documents\FastViewCloudService'
vol_dir = sys.argv[1]
frag_path = sys.argv[2]
meta_line = sys.argv[3]
toc_anchor = sys.argv[4]
toc_add = sys.argv[5]

html_path = os.path.join(fp, vol_dir, vol_dir + '.html')
if not os.path.exists(html_path):
    # try without hyphen
    html_path = os.path.join(fp, vol_dir, vol_dir.replace('-', '') + '.html')
if not os.path.exists(html_path):
    # scan for any html in dir
    import glob
    files = glob.glob(os.path.join(fp, vol_dir, '*.html'))
    if files:
        html_path = files[0]
    else:
        raise SystemExit(f'找不到 {vol_dir} 下的HTML文件')

print(f'目标文件: {html_path}')

frag = open(frag_path, encoding='utf-8').read().strip()
c = open(html_path, encoding='utf-8').read()

# 1) 插入附录片段（紧跟 </main> 之后）
if '</main>' not in c:
    raise SystemExit('找不到 </main> 标签')
pos = c.index('</main>') + len('</main>')
if 'appendix-a' in c:
    print('已存在附录，跳过插入')
else:
    c = c[:pos] + '\n\n' + frag + '\n' + c[pos:]
    print('附录片段已插入')

# 2) 侧边目录：追加附录链接
if toc_anchor in c:
    c = c.replace(toc_anchor, toc_anchor + '\n' + toc_add, 1)
    print('侧边目录已更新')
else:
    print('!! 未找到目录锚点，尝试其他方式...')
    # fallback: find last TOC link and append
    toc_base = '<li><a href="#summary">'
    if toc_base in c:
        pos2 = c.index(toc_base)
        endpos = c.index('</li>', pos2) + 5
        c = c[:endpos] + '\n' + toc_add + c[endpos:]
        print('侧边目录已更新（fallback方式）')
    else:
        print('!! 无法更新侧边目录')

# 3) 更新 meta 行
c, n = re.subn(r'<p class="meta">[^<]*</p>', meta_line, c, count=1)
print('meta 更新 %s 处' % n)

# 备份并写回
bak = html_path + '.bak2'
if not os.path.exists(bak):
    open(bak, 'w', encoding='utf-8').write(open(html_path, encoding='utf-8').read())
    print(f'备份已创建: {bak}')
open(html_path, 'w', encoding='utf-8').write(c)
print(f'写入完成，字节数: {len(c)}')