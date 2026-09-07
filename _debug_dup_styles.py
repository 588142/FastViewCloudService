# -*- coding: utf-8 -*-
"""对比head内style与body内重复style，检查--></script>残迹"""
import re, os

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['economics-lineage', 'psych-lineage', 'math-lineage']

for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    hm = re.search(r'<head(?:\s[^>]*)?>', c)
    head_end = c.find('</head>', hm.end())
    print(f'\n=== {vol} ===')
    
    # head外的style块
    for m in re.finditer(r'<style[^>]*>', c):
        if not (hm.end() <= m.start() < head_end):
            # 提取style块内容
            seg_end = c.find('</style>', m.end())
            block = c[m.start():seg_end + len('</style>')]
            # 在head内找相同或相似块
            head_segs = re.findall(r'<style[^>]*>.*?</style>', c[hm.end():head_end], re.DOTALL)
            line = c[:m.start()].count('\n') + 1
            # 比较：提取块内非空白部分
            core = re.sub(r'\s+', '', block)
            match = None
            for hs in head_segs:
                hcore = re.sub(r'\s+', '', hs)
                if hcore == core:
                    match = '完全相同'
                    break
                # 前缀比较
                if hcore[:200] == core[:200]:
                    match = '前缀相同'
                    break
            print(f'  @line {line}: style块长{len(block)} [{match or "无匹配"}]')
            print(f'    开头: {block[:90].replace(chr(10)," ")}')
    
    # --></script> 残迹
    res = re.findall(r'-->[^<]*</script>', c)
    if res:
        print(f'  ⚠️ --></script>残迹: {len(res)} 处')
        for r in res[:3]:
            idx = c.find(r)
            line = c[:idx].count('\n') + 1
            print(f'    @line {line}: ...{c[max(0,idx-40):idx+30].replace(chr(10)," ")}')
