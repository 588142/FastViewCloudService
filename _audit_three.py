# -*- coding: utf-8 -*-
"""Three.js 3D模型显示专项检查：容器id匹配、高度、渲染器、库引用"""
import os, re

ROOT = r"c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列"

targets = [
    r"心理学思想谱系\心理学思想谱系.html",
    r"数学思想谱系\数学思想谱系.html",
    r"真理的多维图景\真理的多维图景.html",
    r"经济思想谱系\经济思想谱系.html",
    r"经济思想谱系下篇\经济思想谱系下篇.html",
    r"艺术与美学思想谱系\艺术与美学思想谱系.html",
    r"逻辑与论证思想谱系\逻辑与论证思想谱系.html",
    r"马克思主义谱系\马克思主义谱系.html",
    r"..\..\人物索引.html",  # 根目录，用相对路径处理
]
ROOT_INDEX = os.path.join(ROOT, "人物索引.html")

for t in targets:
    if t == r"..\..\人物索引.html":
        fp = ROOT_INDEX
    else:
        fp = os.path.join(ROOT, t)
    if not os.path.exists(fp):
        print(f"!! 不存在: {t}")
        continue
    c = open(fp, encoding='utf-8').read()
    print(f"\n===== {os.path.basename(fp)} =====")
    # 1. 库引用
    libs = re.findall(r'<script[^>]+src="([^"]*(?:three|orbitcontrols)[^"]*)"', c, re.I)
    print(f"  three库引用: {libs if libs else '无(可能CDN)'}")
    cdn = re.findall(r'(https?://[^\s"\'<>]*(?:three[^\s"\'<>]*|orbitcontrols[^\s"\'<>]*))', c, re.I)
    if cdn:
        for u in set(cdn):
            print(f"  CDN: {u[:110]}")
    # 2. 容器
    divs = re.findall(r'<div[^>]*id="([^"]*)"[^>]*>', c)
    three_divs = [d for d in divs if any(k in d.lower() for k in ('three', '3d', 'model', 'scene', 'globe', 'webgl'))]
    print(f"  div容器总数: {len(divs)}, 疑似3D容器: {three_divs}")
    # 3. JS引用容器
    getids = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', c))
    qs = set(re.findall(r'\$\("#([^"]+)"\)', c))
    jsrefs = getids | qs
    three_refs = [r for r in jsrefs if any(k in r.lower() for k in ('three', '3d', 'model', 'scene', 'globe', 'webgl', 'container', 'mount'))]
    print(f"  JS引用的容器: {three_refs if three_refs else jsrefs if jsrefs else '无'}")
    # 4. 高度检查：容器 style/class
    for d in three_divs:
        m = re.search(r'<div[^>]*id="' + re.escape(d) + r'"[^>]*>', c)
        if m:
            seg = m.group(0)
            h = re.search(r'height\s*:\s*([^;"\']+)', seg)
            cls = re.search(r'class="([^"]*)"', seg)
            print(f"  div#{d}: style高度={h.group(1) if h else '未内联'}, class={cls.group(1) if cls else ''}")
    # 5. 渲染器与尺寸
    for kw in ('WebGLRenderer', 'PerspectiveCamera', 'OrbitControls', 'setSize', 'requestAnimationFrame', 'animate'):
        print(f"  {kw}: {'有' if kw in c else '无'}")
    # 6. 内联style中3D容器高度
    hs = re.findall(r'#([\w-]+)\s*\{[^}]*height\s*:\s*([0-9.]+)(px|vh|%)', c)
    print(f"  含height的CSS规则: {[(a,b+e) for a,b,e in hs][:6]}")
