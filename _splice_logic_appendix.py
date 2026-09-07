# -*- coding: utf-8 -*-
import os, re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\logic-lineage\logic-lineage.html'
frag_path = r'c:\Users\Admin1\Documents\FastViewCloudService\_logic_appendix_fragment.html'

frag = open(frag_path, encoding='utf-8').read().strip()
c = open(fp, encoding='utf-8').read()

# 1) 插入附录片段（紧跟 </main> 之后，位于“关联辑目”之前）
if '</main>' not in c:
    raise SystemExit('找不到 </main>')
pos = c.index('</main>') + len('</main>')
if 'appendix-a' in c:
    print('已存在附录，跳过插入')
else:
    c = c[:pos] + '\n\n' + frag + '\n' + c[pos:]

# 2) 侧边目录：在第七章之后追加附录链接
toc_anchor = '<li><a href="#summary">第七章 · 总结提炼：逻辑的启示</a></li>'
toc_add = toc_anchor + '''
      <li style="margin-top:0.9rem;font-weight:700;color:var(--accent2);font-size:0.8rem;">★ 本科生升级附录</li>
      <li><a href="#appendix-a">附录一 · 导览与教材对标</a></li>
      <li><a href="#appendix-b">附录二 · 精确定义与术语表</a></li>
      <li><a href="#appendix-c">附录三 · 命题逻辑与真值表</a></li>
      <li><a href="#appendix-d">附录四 · 自然演绎与证明</a></li>
      <li><a href="#appendix-e">附录五 · 三段论：格与式</a></li>
      <li><a href="#appendix-f">附录六 · 谓词逻辑与哥德尔</a></li>
      <li><a href="#appendix-g">附录七 · 自然语言符号化</a></li>
      <li><a href="#appendix-h">附录八 · 经典习题集</a></li>
      <li><a href="#appendix-i">附录九 · 一手文献选读</a></li>
      <li><a href="#appendix-j">附录十 · 关键争论</a></li>
      <li><a href="#appendix-k">附录十一 · 延伸阅读与课程</a></li>'''
if toc_anchor in c:
    c = c.replace(toc_anchor, toc_add, 1)
    print('侧边目录已更新')
else:
    print('!! 未找到第七章目录锚点')

# 3) 更新 meta 行
new_meta = '<p class="meta">作者：詹家杨 · 2026-09-06 · 8 张思维导图 · 7 张对照表 · 30+ 人物语录 · 11 个本科升级附录（术语表 · 真值表 · 自然演绎 · 习题集 · 文献选读）</p>'
c, n = re.subn(r'<p class="meta">[^<]*</p>', new_meta, c, count=1)
print('meta 更新 %s 处' % n)

# 备份并写回
open(fp + '.bak2', 'w', encoding='utf-8').write(open(fp, encoding='utf-8').read())
open(fp, 'w', encoding='utf-8').write(c)
print('写入完成，字节数：', len(c))