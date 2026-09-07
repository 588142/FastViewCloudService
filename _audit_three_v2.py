# -*- coding: utf-8 -*-
"""3D模型/图表显示综合检查 v2：
1. JS引用的每个容器id 在HTML中必须存在（任意标签）
2. 容器或其包裹层必须有有效高度
3. id不能重复
4. getElementById 后必须判空再使用
5. script块括号粗平衡
"""
import os, re

ROOT = r"c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列"

THREE_FILES = [
    r"心理学思想谱系\心理学思想谱系.html",
    r"数学思想谱系\数学思想谱系.html",
    r"真理的多维图景\真理的多维图景.html",
    r"经济思想谱系\经济思想谱系.html",
    r"经济思想谱系下篇\经济思想谱系下篇.html",
    r"逻辑与论证思想谱系\逻辑与论证思想谱系.html",
    r"马克思主义谱系\马克思主义谱系.html",
]

def get_els(c, tag):
    """返回 {id: {inline_style, class}}"""
    out = {}
    # 匹配 <tag ... id="x" ...> 属性顺序任意
    for m in re.finditer(r'<%s\b([^>]*)>' % tag, c):
        attrs = m.group(1)
        mid = re.search(r'id=["\']([^"\']+)["\']', attrs)
        if not mid:
            continue
        style = re.search(r'style=["\']([^"\']*)["\']', attrs)
        cls = re.search(r'class=["\']([^"\']*)["\']', attrs)
        out[mid.group(1)] = {
            'style': style.group(1) if style else '',
            'class': cls.group(1) if cls else '',
        }
    return out

def css_heights(c):
    """提取所有 #id / .class 的 height 规则"""
    hs = {}
    for m in re.finditer(r'([#.][\w-]+)\s*\{([^}]*)\}', c):
        body = m.group(2)
        hm = re.search(r'height\s*:\s*([^;]+);', body)
        if hm:
            hs[m.group(1)] = hm.group(1).strip()
    return hs

def check(fp, label):
    c = open(fp, encoding='utf-8').read()
    print(f"\n===== {label} =====")
    all_els = {}
    for tag in ('div', 'canvas', 'section', 'span', 'figure'):
        all_els.update(get_els(c, tag))
    css_h = css_heights(c)
    # 1. JS 引用的 id
    jsrefs = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', c))
    jsrefs |= set(re.findall(r'\$\("#([^"]+)"\)', c))
    # 只保留与可视化相关的（去掉明显的 UI 控件类）
    issues = []
    for rid in sorted(jsrefs):
        if rid in ('backTop',):
            continue
        if rid not in all_els:
            issues.append(f"  [缺容器] JS引用 {rid} 但HTML无此元素")
            continue
        el = all_els[rid]
        h_ok = False
        if re.search(r'height\s*:', el['style'], re.I):
            h_ok = True
        # 包裹类：viz-container / three-wrap / phd-three-container / viz-canvas
        for sel, h in css_h.items():
            if sel == '#' + rid and 'height' in sel + 'h':
                pass
        # class 或父级 class 高度
        for sel, h in css_h.items():
            if sel.startswith('.'):
                cn = sel[1:]
                if cn in el['class'].split():
                    h_ok = True
        if not h_ok:
            issues.append(f"  [无高度] #{rid} (tag含canvas/div, class={el['class'] or '-'}, style={el['style'] or '-'})")
    # 2. id 重复
    seen = {}
    for tag in ('div', 'canvas', 'section'):
        for idv in get_els(c, tag):
            seen[idv] = seen.get(idv, 0) + 1
    dups = [k for k, v in seen.items() if v > 1 and any(x in k.lower() for x in ('3d', 'chart', 'canvas', 'viz', 'three'))]
    for d in dups:
        issues.append(f"  [id重复] {d} 出现{seen[d]}次")
    # 3. getElementById 判空
    # 简单检查: 找 "var X = document.getElementById(...)" 后 500 字符内是否出现 if (!X / if(X===null) / if (X == null)
    for m in re.finditer(r'var\s+(\w+)\s*=\s*document\.getElementById\(["\']([^"\']+)["\']\)', c):
        var, rid = m.group(1), m.group(2)
        if not any(x in rid.lower() for x in ('3d', 'viz', 'chart', 'three', 'canvas', 'model', 'globe', 'scene')):
            continue
        tail = c[m.end():m.end() + 400]
        if not re.search(r'if\s*\(\s*!?' + re.escape(var), tail) and not re.search(r'if\s*\(\s*' + re.escape(var) + r'\s*[=!]==?\s*null', tail):
            issues.append(f"  [未判空] {var}=getElementById('{rid}') 后未判空")
    # 4. script 括号平衡
    for i, m in enumerate(re.finditer(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', c, re.S)):
        js = m.group(1)
        bal = js.count('{') - js.count('}')
        if bal != 0:
            issues.append(f"  [JS括号] script#{i} 花括号不平衡 diff={bal}")
    if issues:
        for x in issues:
            print(x)
    else:
        print("  ✓ 全部通过（容器存在/高度/无重复/判空/括号平衡）")
    # 输出容器清单
    print("  3D容器:", [k for k in sorted(all_els) if '3d' in k.lower() or 'three' in k.lower()][:12])

for f in THREE_FILES:
    check(os.path.join(ROOT, f), os.path.basename(f))
