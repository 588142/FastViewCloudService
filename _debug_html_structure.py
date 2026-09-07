# -*- coding: utf-8 -*-
"""检查 marxism 文件的所有结构问题"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
fp = os.path.join(ws, 'marxism-lineage', 'marxism-lineage.html')
c = open(fp, encoding='utf-8').read()

# 1. 所有 </html> 位置
print('=== </html> 出现位置 ===')
for m in re.finditer(r'</html>', c):
    print(f'  @ {m.start()}')

# 2. 所有 </body> 位置
print('\n=== </body> 出现位置 ===')
for m in re.finditer(r'</body>', c):
    print(f'  @ {m.start()}')

# 3. 所有 <footer 位置
print('\n=== <footer 出现位置 ===')
for m in re.finditer(r'<footer', c):
    ctx = c[m.start():m.start()+100]
    print(f'  @ {m.start()}: {ctx[:80]}')

# 4. 所有 <body 和 </article> </div> 关键结构
print('\n=== 关键结构标记 ===')
for tag in ['<body', '</article>', 'class="shell"', '<div class="shell">']:
    positions = [m.start() for m in re.finditer(re.escape(tag), c)]
    print(f'  {tag}: {len(positions)} 处 {positions[:10]}')

# 5. 检查 masters-prologue 和 phd 部分之间结构
print('\n=== masters-prologue @ 105215 附近 ===')
print(c[105215:105500])

print('\n=== phd-prologue @ 142861 附近 ===')
print(c[142861:143100])

# 6. 找 footer 和 第一个 </html> 之间的内容
print('\n=== 第一个footer到第一个</html> ===')
first_html = c.find('</html>')
print(c[first_html-1500:first_html+50])