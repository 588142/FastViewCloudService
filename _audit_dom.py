# -*- coding: utf-8 -*-
"""基于 html.parser 的 DOM 结构 + 可视化显示检查：
1. 标签闭合平衡
2. id 唯一性
3. JS 引用的每个 id 必须存在于 DOM
4. 可视化容器（3d/chart/canvas/viz/three/model/globe/scene）必须有有效高度（自身或祖先链）
单遍解析，O(1) 出栈，适合大文件。
"""
import os, re, sys
from html.parser import HTMLParser

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"c:\Users\Admin1\Documents\FastViewCloudService\思想图谱系列"
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
VIZ_RE = re.compile(r'(3d|chart|canvas|viz|three|globe|model|scene)', re.I)

class DomCheck(HTMLParser):
    CDATA_CONTENT_ELEMENTS = ("script", "style")

    def __init__(self, css_rules):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.all_ids = {}
        self.errors = []
        self.css = css_rules
        self.viz = {}          # id -> 高度来源
        self.viz_noheight = [] # id 列表

    def _style(self, attrs):
        return attrs.get('style') or ''

    def _classes(self, attrs):
        return (attrs.get('class') or '').split()

    def height_of(self, attrs):
        st = self._style(attrs)
        if re.search(r'height\s*:', st, re.I):
            return 'inline'
        if attrs.get('height'):
            return f'attr height={attrs["height"]}'
        for c in self._classes(attrs):
            if self.css.get('.' + c, {}).get('height'):
                return f'.{c}'
            if self.css.get('.' + c + ' canvas', {}).get('height'):
                return f'.{c} canvas'
        i = attrs.get('id')
        if i and self.css.get('#' + i, {}).get('height'):
            return f'#{i}'
        if i and self.css.get('#' + i + ' canvas', {}).get('height'):
            return f'#{i} canvas'
        for t, a in reversed(self.stack):
            st2 = self._style(a)
            if re.search(r'height\s*:', st2, re.I):
                return f'父级inline'
            if a.get('height'):
                return f'父级attr'
            for c in self._classes(a):
                if self.css.get('.' + c, {}).get('height'):
                    return f'父级.{c}'
                if self.css.get('.' + c + ' canvas', {}).get('height'):
                    return f'父级.{c} canvas'
            i2 = a.get('id')
            if i2 and self.css.get('#' + i2, {}).get('height'):
                return f'父级#{i2}'
            if i2 and self.css.get('#' + i2 + ' canvas', {}).get('height'):
                return f'父级#{i2} canvas'
        return None

    def _on_open(self, attrs):
        i = attrs.get('id')
        if i:
            self.all_ids[i] = self.all_ids.get(i, 0) + 1
            if VIZ_RE.search(i):
                h = self.height_of(attrs)
                if h:
                    self.viz[i] = h
                else:
                    self.viz_noheight.append(i)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, attrs))
        self._on_open(attrs)

    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)
        self._on_open(attrs)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        for idx in range(len(self.stack) - 1, -1, -1):
            if self.stack[idx][0] == tag:
                skipped = [t for t, _ in self.stack[idx:]]
                self.errors.append(f"  </{tag}> 闭合时中间未闭合: {skipped[:8]}")
                del self.stack[idx:]
                return
        self.errors.append(f"  多余闭合 </{tag}>")

def extract_css(c):
    # 仅提取 <style> 块，避免正则扫描内联 JS 导致灾难性回溯
    styles = re.findall(r'<style[^>]*>(.*?)</style>', c, flags=re.S | re.I)
    c = re.sub(r'/\*.*?\*/', '', '\n'.join(styles), flags=re.S)
    rules = {}
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', c):
        sels = [s.strip() for s in m.group(1).split(',')]
        body = m.group(2)
        props = {}
        for pm in re.finditer(r'([\w-]+)\s*:\s*([^;]+);', body):
            props[pm.group(1).strip()] = pm.group(2).strip()
        if 'height' in props:
            for s in sels:
                if s:
                    rules[s] = props
    return rules

def all_html():
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        if any(p in ('_shared', 'assets') for p in rel.split(os.sep)):
            continue
        for f in fn:
            if f.endswith('.html'):
                yield os.path.join(dp, f), os.path.relpath(os.path.join(dp, f), ROOT)

total_bad = 0
for f, rel in sorted(all_html()):
    fp = os.path.join(ROOT, f)
    c = open(fp, encoding='utf-8').read()
    css = extract_css(c)
    p = DomCheck(css)
    try:
        p.feed(c); p.close()
    except Exception as e:
        p.errors.append(f"  [解析异常] {e}")
    print(f"===== {rel} =====")
    ok = True
    if not p.errors and not p.stack:
        print("  ✓ 标签闭合平衡")
    else:
        ok = False
        for e in p.errors[:8]:
            print(f"  {e}")
        if p.stack:
            unclosed = [t for t, a in p.stack if t not in VOID]
            print(f"  未闭合标签 {len(unclosed)} 个: {unclosed[:10]}")
    dups = {k: v for k, v in p.all_ids.items() if v > 1}
    if dups:
        ok = False
        print(f"  [id重复] {dups}")
    jsrefs = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', c))
    jsrefs |= set(re.findall(r'\$\("#([^"]+)"\)', c))
    jsrefs -= {'backTop'}
    dyn_ids = set()
    for m in re.finditer(r"innerHTML\s*=\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|`[^`]*`)", c, flags=re.S):
        dyn_ids |= set(re.findall(r'id="([^"]+)"', m.group(1)))
    missing = [r for r in sorted(jsrefs) if p.all_ids.get(r, 0) == 0 and r not in dyn_ids]
    if missing:
        ok = False
        print(f"  [JS引用缺元素] {missing}")
    if p.viz_noheight:
        ok = False
        print(f"  [可视化容器无高度] {p.viz_noheight}")
    if ok:
        print(f"  ✓ 全部通过（可视化容器 {len(p.viz)} 个）")
    total_bad += 0 if ok else 1

print(f"\n========== 汇总: {total_bad} 个文件存在问题 ==========")
