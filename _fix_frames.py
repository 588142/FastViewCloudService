# -*- coding: utf-8 -*-
"""修复7个标星卷的多重文档框架问题
方案：删除多余框架标签（DOCTYPE/html/head/body），移动模块style到主head，
     修复悬空'关联辑目'section位置。所有内容保持原位。
"""
import re, os, shutil

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']


def extract_section_ids(c):
    return re.findall(r'<section[^>]*id="([^"]*)"', c)


def fix_volume(vol):
    fp = os.path.join(ws, vol, vol + '.html')
    c = open(fp, encoding='utf-8').read()
    orig_len = len(c)
    orig_sections = extract_section_ids(c)

    # === 1. 提取所有 style 块（按出现顺序） ===
    styles = re.findall(r'<style[^>]*>.*?</style>', c, re.DOTALL)
    n_styles = len(styles)

    # === 2. 定位主 head ===
    # 主head: 第一个真正 <head> 到第一个 </head>
    head_m = re.search(r'<head(?:\s[^>]*)?>', c)
    assert head_m, f'{vol}: 找不到主head'
    main_head_start = head_m.start()
    main_head_end_tag = c.find('</head>', head_m.end())
    assert main_head_end_tag != -1, f'{vol}: 找不到主head闭合'
    main_head_content = c[head_m.end():main_head_end_tag]

    # 提取主head内的style（用于从styles列表中识别）
    main_head_styles = re.findall(r'<style[^>]*>.*?</style>', main_head_content, re.DOTALL)
    n_main_styles = len(main_head_styles)

    # 非主style = 全部styles - 主head内的
    # 注意：主head外的style按原顺序，但主head内的style保留在原位
    # 所以：先删掉主head外的所有style块，再在 </head> 前统一插入（含主head的？不，主head的已在head内）
    non_main_styles = []
    # 遍历styles，跳过在主head范围内的
    for s in styles:
        s_pos = c.find(s)
        if not (main_head_start <= s_pos < main_head_end_tag):
            non_main_styles.append(s)

    # === 3. 提取主 head 的 meta/title ===
    metas = re.findall(r'<meta[^>]*>', main_head_content)
    title_m = re.search(r'<title>.*?</title>', main_head_content, re.DOTALL)
    title = title_m.group(0) if title_m else '<title></title>'

    # === 4. 提取"关联辑目" section（如果有） ===
    gj_pat = re.compile(r'<section[^>]*>\s*<h2>\s*关联辑目.*?</section>', re.DOTALL)
    gj_m = gj_pat.search(c)
    gj_block = gj_m.group(0) if gj_m else None

    # === 5. 删除非主框架标签 ===
    # 5a. 删除非主 DOCTYPE（保留第一个）
    c_new = c
    doctypes = [m.start() for m in re.finditer(r'<!DOCTYPE[^>]*>', c_new, re.IGNORECASE)]
    if len(doctypes) > 1:
        for pos in reversed(doctypes[1:]):
            # 删除该位置开始的DOCTYPE
            m = re.search(r'<!DOCTYPE[^>]*>', c_new[pos:])
            c_new = c_new[:pos] + c_new[pos+m.end():]

    # 5b. 删除非主 <html> 标签（保留第一个）
    htmls = [m for m in re.finditer(r'<html(?:\s[^>]*)?>', c_new)]
    if len(htmls) > 1:
        for m in reversed(htmls[1:]):
            c_new = c_new[:m.start()] + c_new[m.end():]

    # 5c. 删除非主 </html>（保留最后一个）
    html_closes = [m.start() for m in re.finditer(r'</html>', c_new)]
    if len(html_closes) > 1:
        for pos in reversed(html_closes[:-1]):
            c_new = c_new[:pos] + c_new[pos+len('</html>'):]

    # 5d. 删除非主 <head>...</head> 块（保留第一个真正head）
    # 先找到主head的结束位置（在c_new中）
    head_m2 = re.search(r'<head(?:\s[^>]*)?>', c_new)
    main_head_end2 = c_new.find('</head>', head_m2.end())
    # 找到所有head块
    head_blocks = list(re.finditer(r'<head(?:\s[^>]*)?>.*?</head>', c_new, re.DOTALL))
    if len(head_blocks) > 1:
        for m in reversed(head_blocks[1:]):
            c_new = c_new[:m.start()] + c_new[m.end():]

    # 5e. 删除非主 <body> 标签（保留第一个）
    bodies = [m for m in re.finditer(r'<body(?:\s[^>]*)?>', c_new)]
    if len(bodies) > 1:
        for m in reversed(bodies[1:]):
            c_new = c_new[:m.start()] + c_new[m.end():]

    # 5f. 删除非主 </body>（保留最后一个）
    body_closes = [m.start() for m in re.finditer(r'</body>', c_new)]
    if len(body_closes) > 1:
        for pos in reversed(body_closes[:-1]):
            c_new = c_new[:pos] + c_new[pos+len('</body>'):]

    # === 6. 插入非主 style 到主 </head> 前 ===
    # 重新定位主 </head>
    head_m3 = re.search(r'<head(?:\s[^>]*)?>', c_new)
    main_head_end3 = c_new.find('</head>', head_m3.end())
    style_insert = '\n\n  <!-- 各升级模块样式（原内嵌head，已合并） -->\n' + '\n'.join(non_main_styles) + '\n'
    c_new = c_new[:main_head_end3] + style_insert + c_new[main_head_end3:]

    # === 7. 移动"关联辑目" section 到主 </main> 之后 ===
    if gj_block:
        # 从当前位置删除
        c_new = c_new.replace(gj_block, '', 1)
        # 插入到 </main> 之后（主main闭合）
        main_close = c_new.find('</main>')
        if main_close != -1:
            insert_pos = main_close + len('</main>')
            c_new = c_new[:insert_pos] + '\n\n' + gj_block + '\n' + c_new[insert_pos:]
        else:
            print(f'  ⚠️ {vol}: 找不到</main>，关联辑目未移动')

    # === 8. 验证 ===
    new_sections = extract_section_ids(c_new)
    checks = {
        'DOCTYPE': len(re.findall(r'<!DOCTYPE', c_new, re.IGNORECASE)),
        '<html': len(re.findall(r'<html(?:\s[^>]*)?>', c_new)),
        '</html>': len(re.findall(r'</html>', c_new)),
        '<head': len(re.findall(r'<head(?:\s[^>]*)?>', c_new)),
        '<body': len(re.findall(r'<body(?:\s[^>]*)?>', c_new)),
        '</body>': len(re.findall(r'</body>', c_new)),
    }
    sec_ok = len(new_sections) == len(orig_sections)
    size_ok = abs(len(c_new) - orig_len) < 5000  # 大小基本不变（删除框架+添加style）

    print(f'\n=== {vol} ===')
    print(f'  原大小: {orig_len} → 新大小: {len(c_new)}')
    print(f'  style块: 总{n_styles} (主head内{n_main_styles} + 移动{len(non_main_styles)})')
    print(f'  section: {len(orig_sections)} → {len(new_sections)} {"✓" if sec_ok else "✗"}')
    print(f'  框架标签: {checks}')
    
    ok = all(v == 1 for v in checks.values()) and sec_ok
    if ok:
        # 备份并写回
        bak = fp + '.bak'
        if not os.path.exists(bak):
            shutil.copy2(fp, bak)
        open(fp, 'w', encoding='utf-8').write(c_new)
        print(f'  ✅ 修复完成并写回')
    else:
        print(f'  ⚠️ 验证未通过，未写回')
    return ok


if __name__ == '__main__':
    results = {}
    for vol in vols:
        results[vol] = fix_volume(vol)
    print(f'\n{"="*60}')
    print(f'成功: {sum(results.values())}/{len(vols)}')
    for vol, ok in results.items():
        print(f'  {vol}: {"✅" if ok else "❌"}')