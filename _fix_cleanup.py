# -*- coding: utf-8 -*-
"""清理script残迹(--></script>)和body内重复style块"""
import re, os, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

# ===== 1. 清理 --></script> 残迹 =====
print('=== 1. 清理script残迹 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    orig = c
    # 模式：注释结束-->后跟1个或多个>再</script>（修复脚本遗留）
    c = re.sub(r'(<!-- (?:three\.min\.js|chart\.js) 已在上方加载 -->)>+\s*</script>', r'\1', c)
    # 通用残迹：-->后紧跟</script>（前面有对应script开标签被注释掉的）
    # 先看是否有其他模式
    others = re.findall(r'-->[^<]*</script>', c)
    n = len(re.findall(r'</script>', orig)) - len(re.findall(r'</script>', c))
    if c != orig:
        bak = fp + '.bak2'
        if not os.path.exists(bak):
            shutil.copy2(fp, bak)
        open(fp, 'w', encoding='utf-8').write(c)
        print(f'  {vol}: 修复{n}处残迹')
    else:
        print(f'  {vol}: 无残迹')
    if others:
        print(f'    ⚠️ 仍残留: {others[:2]}')

# ===== 2. 删除body内重复style块（与head内完全相同） =====
print('\n=== 2. 删除重复style块 ===')
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    hm = re.search(r'<head(?:\s[^>]*)?>', c)
    head_end = c.find('</head>', hm.end())
    head_segs = re.findall(r'<style[^>]*>.*?</style>', c[hm.end():head_end], re.DOTALL)
    head_cores = [re.sub(r'\s+', '', hs) for hs in head_segs]

    # 收集所有style块（含body内的）
    removed = 0
    for m in re.finditer(r'<style[^>]*>.*?</style>', c, re.DOTALL):
        if hm.end() <= m.start() < head_end:
            continue  # head内的保留
        core = re.sub(r'\s+', '', m.group(0))
        if core in head_cores:
            c = c[:m.start()] + '<!-- 重复样式已合并至head -->' + c[m.end():]
            removed += 1

    if removed:
        # 再次确认style数
        n_after = len(re.findall(r'<style', c))
        print(f'  {vol}: 删除{removed}个重复style块, 剩余style={n_after}')
        open(fp, 'w', encoding='utf-8').write(c)
    else:
        print(f'  {vol}: 无重复style块')

print('\n完成')
