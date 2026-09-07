# -*- coding: utf-8 -*-
"""最终确认：旧版重复文件是否被活动页面引用"""
import os, re, glob

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
dt = r'c:\Users\Admin1\Desktop\Trae资料库'

# 桌面版旧版重复文件清单
stale_files = [
    ('艺术与美学思想谱系', 'art-aesthetics.html'),
    ('东方思想谱系', 'eastern-thought.html'),
    ('经济思想谱系', 'econ-thought.html'),
    ('教育思想谱系', 'edu-lineage.html'),
]

print('=== 检查这些旧版重复文件是否被活动页面引用 ===')
for cn, fname in stale_files:
    target = os.path.normpath(os.path.join(dt, cn, fname))
    refs = []
    for hf in glob.glob(os.path.join(dt, '**', '*.html'), recursive=True):
        if '_backup_before_merge' in hf:
            continue
        try:
            c = open(hf, encoding='utf-8').read()
        except Exception:
            continue
        base = os.path.dirname(hf)
        for m in re.finditer(r'href="([^"#]+?\.html)"', c):
            href = m.group(1)
            if href.startswith(('http', 'mailto')):
                continue
            full = os.path.normpath(os.path.join(base, href))
            if full == target:
                refs.append(os.path.relpath(hf, dt))
    if refs:
        print('  {} {} 仍被 {} 引用!!'.format(cn, fname, len(refs)))
        for r in refs[:8]:
            print('      <-', r)
    else:
        print('  [无引用] {}/{}'.format(cn, fname))

print()
print('=== 工作区 _masters_logic-lineage.html 头部 ===')
mf = os.path.join(ws, '_masters_logic-lineage.html')
if os.path.exists(mf):
    c = open(mf, encoding='utf-8').read()
    print('  大小:', len(c), '字符')
    print('  前300字符:', c[:300].replace('\n', ' '))
    print('  Title:', re.search(r'<title>(.*?)</title>', c, re.S).group(1)[:80] if re.search(r'<title>(.*?)</title>', c, re.S) else 'N/A')
