# -*- coding: utf-8 -*-
"""按顺序定位每个未闭合div，显示完整结构"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 直接在原始文件上做div栈追踪，记录每个未闭合div的绝对位置和attrs
stack = []
unclosed = []
for m in re.finditer(r'<(/?)(div)((?:\s[^>]*)?)(/?)>', c):
    closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) or '', m.group(4)
    if selfclose:
        continue
    if not closing:
        stack.append((m.start(), attrs.strip()[:80]))
    else:
        if stack:
            stack.pop()

unclosed = stack
print(f'未闭合: {len(unclosed)}\n')

# 按顺序显示每个未闭合div的完整内容（开标签 → 下一个同级section边界）
# 为每个div找"内容结束"：下一个 </section> 或 </main> 或 </article>
prev_end = 0
for i, (pos, attrs) in enumerate(unclosed):
    line = c[:pos].count('\n') + 1
    # 该div的"理论结束点"：下一个 </section>
    sec = c.find('</section>', pos)
    end = sec if sec != -1 else c.find('</main>', pos)
    seg = c[pos:end]
    # 打印结构骨架：只显示标签行（去内容）
    skeleton = re.sub(r'>[^<>]*<', '><', seg)
    print(f'===== [{i+1}] <div {attrs}> @ line {line} (内容{len(seg)}字符) =====')
    print(skeleton[:900])
    print()
