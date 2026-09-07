# -*- coding: utf-8 -*-
import os, re, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'

# Volume configs: (dir, html_file, appendix_fragment, toc_anchor, new_meta)
configs = [
    ('truth-dimensions', 'truth-dimensions.html',
     '_appendix_truth-dimensions.html',
     '<li><a href="#synthesis">第七章 · 总结：谁有资格判定真</a></li>',
     '<p class="meta">作者：詹家杨 · 2026-09-06 · 8 张思维导图 · 6 张对照表 · 30+ 人物语录 · 11 个本科升级附录（术语表 · 真理空间模型 · 函数曲线 · 习题集 · 文献选读）</p>'),

    ('marxism-lineage', 'marxism-lineage.html',
     '_appendix_marxism-lineage.html',
     '<li><a href="#summary">第七章 · 总结：源与流</a></li>',
     '<p class="meta">作者：詹家杨 · 2026-09-06 · 10 张思维导图 · 4 张对照表 · 30+ 人物语录 · 11 个本科升级附录（术语表 · 唯物史观3D模型 · 生产力曲线 · 习题集 · 文献选读）</p>'),

    ('economics-lineage', 'economics-lineage.html',
     '_appendix_economics-lineage.html',
     '<li><a href="#formulas">第七章 · 总结 · 常用经济公式速查</a></li>',
     '<p class="meta">作者：詹家杨 · 2026-09-06 · 6 张思维导图 · 2 张对照表 · 20+ 常用经济公式 · 30+ 人物语录 · 11 个本科升级附录（术语表 · 供需3D曲面 · 生产函数 · 习题集 · 文献选读）</p>'),

    ('econ-part2-lineage', 'econ-part2-lineage.html',
     '_appendix_econ-part2-lineage.html',
     '<li><a href="#summary">第六章 · 总结提炼：当代经济的启示</a></li>',
     '<p class="meta">作者：詹家杨 · 2026-09-06 · 7 张思维导图 · 7 张对照表 · 30+ 人物语录 · 当代经济前沿 · 11 个本科升级附录（术语表 · IS-LM-BP 3D模型 · 菲利普斯曲线 · 习题集 · 文献选读）</p>'),

    ('psych-lineage', 'psych-lineage.html',
     '_appendix_psych-lineage.html',
     '<li><a href="#summary">第六章 · 总结提炼：心理学的启示</a></li>',
     '<p class="meta">作者：詹家杨 · 2026-09-06 · 8 张思维导图 · 9 张对照表 · 30+ 人物语录 · 11 个本科升级附录（术语表 · 人格3D模型 · ROC曲线 · 学习曲线 · 习题集 · 文献选读）</p>'),

    ('math-lineage', 'math-lineage.html',
     '_appendix_math-lineage.html',
     '<li><a href="#summary">第七章 · 总结提炼：数学的启示</a></li>',
     '<p class="meta">作者：詹家杨 · 2026-09-06 · 8 张思维导图 · 7 张对照表 · 20+ 人物语录 · 11 个本科升级附录（术语表 · 3D曲面 · 函数族对比 · 极限逼近 · 习题集 · 文献选读）</p>'),
]

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

for vol_dir, html_file, frag_name, toc_anchor, new_meta in configs:
    html_path = os.path.join(ws, vol_dir, html_file)
    frag_path = os.path.join(ws, frag_name)
    
    print(f'\n{"="*60}')
    print(f'处理: {vol_dir}')
    print(f'目标: {html_path}')
    
    if not os.path.exists(html_path):
        print(f'!! 文件不存在: {html_path}')
        continue
    
    frag = open(frag_path, encoding='utf-8').read().strip()
    c = open(html_path, encoding='utf-8').read()
    
    # 1) 插入附录片段
    if '</main>' not in c:
        print('!! 找不到 </main>')
        continue
    pos = c.index('</main>') + len('</main>')
    
    if 'appendix-a' in c:
        print('已存在附录，跳过插入')
    else:
        c = c[:pos] + '\n\n' + frag + '\n' + c[pos:]
        print('附录片段已插入')
    
    # 2) 更新侧边目录
    if toc_anchor in c:
        c = c.replace(toc_anchor, toc_anchor + '\n' + toc_append, 1)
        print(f'侧边目录已更新 (锚点: {toc_anchor[:40]}...)')
    else:
        print(f'!! 未找到TOC锚点: {toc_anchor[:40]}...')
        # 尝试找最后一个TOC链接
        all_links = re.findall(r'<li><a href="#[^"]*">[^<]*</a></li>', c)
        if all_links:
            last = all_links[-1]
            c = c.replace(last, last + '\n' + toc_append, 1)
            print(f'  fallback: 使用最后一个TOC链接 {last[:40]}...')
    
    # 3) 更新meta行
    old_meta = re.search(r'<p class="meta">[^<]*</p>', c)
    if old_meta:
        c = c.replace(old_meta.group(0), new_meta, 1)
        print('meta行已更新')
    else:
        print('!! 未找到meta行')
    
    # 备份并写回
    bak = html_path + '.bak2'
    if not os.path.exists(bak):
        shutil.copy2(html_path, bak)
        print(f'备份已创建')
    
    open(html_path, 'w', encoding='utf-8').write(c)
    new_size = len(c)
    print(f'写入完成，新大小: {new_size} 字节 ({new_size/1024:.0f}KB)')

print('\n' + '='*60)
print('全部拼接完成！')