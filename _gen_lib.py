# -*- coding: utf-8 -*-
"""思想图谱系列 · 新辑生成器模板库"""

CSS = """
    @font-face {
      font-family: 'Lora';
      src: url('./_shared/fonts/Lora-Regular.ttf') format('truetype');
      font-weight: 400;
    }
    @font-face {
      font-family: 'Lora';
      src: url('./_shared/fonts/Lora-Bold.ttf') format('truetype');
      font-weight: 700;
    }
    @font-face {
      font-family: 'Lora';
      src: url('./_shared/fonts/Lora-Italic.ttf') format('truetype');
      font-weight: 400;
      font-style: italic;
    }
    @font-face {
      font-family: 'WorkSans';
      src: url('./_shared/fonts/WorkSans-Regular.ttf') format('truetype');
      font-weight: 400;
    }
    @font-face {
      font-family: 'WorkSans';
      src: url('./_shared/fonts/WorkSans-Bold.ttf') format('truetype');
      font-weight: 700;
    }
    @font-face {
      font-family: 'DMMono';
      src: url('./_shared/fonts/DMMono-Regular.ttf') format('truetype');
      font-weight: 400;
    }
"""

CSS_BODY = """
    :root {{
      --bg: #FBF8F3;
      --bg2: #F3EDE1;
      --ink: #2B2418;
      --muted: #6E6352;
      --rule: #E4DBC9;
      --accent: {accent};
      --accent2: {accent2};
      --font-head: 'Lora', 'Songti SC', 'SimSun', serif;
      --font: 'WorkSans', 'PingFang SC', 'Microsoft YaHei', sans-serif;
      --font-mono: 'DMMono', monospace;
      --max: 880px;
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ font-size: 16px; scroll-behavior: smooth; }}
    body {{
      font-family: var(--font);
      color: var(--ink);
      background: var(--bg);
      line-height: 1.75;
    }}

    .shell {{ display: grid; grid-template-columns: 250px minmax(0, 1fr); gap: 2.5rem; max-width: 1220px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .sidenav {{ position: sticky; top: 2rem; align-self: start; max-height: calc(100vh - 4rem); overflow-y: auto; }}
    .sidenav .brand {{ font-family: var(--font-head); font-size: 1.05rem; font-weight: 700; margin-bottom: 0.25rem; }}
    .sidenav .brand-sub {{ font-size: 0.78rem; color: var(--muted); margin-bottom: 1rem; }}
    .searchbox {{ width: 100%; padding: 0.5rem 0.7rem; font: 400 0.85rem var(--font); color: var(--ink); background: var(--bg); border: 1px solid var(--rule); border-radius: 8px; margin-bottom: 1.2rem; }}
    .searchbox:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
    .toc {{ list-style: none; font-size: 0.85rem; }}
    .toc li {{ margin-bottom: 0.15rem; }}
    .toc a {{ display: block; padding: 0.35rem 0.6rem; color: var(--muted); text-decoration: none; border-left: 2px solid var(--rule); }}
    .toc a:hover, .toc a.active {{ color: var(--accent); border-left-color: var(--accent); background: var(--bg2); }}

    article.page {{ max-width: var(--max); }}

    header.masthead {{ border-bottom: 2px solid var(--ink); padding-bottom: 1.5rem; margin-bottom: 2.5rem; }}
    .kicker {{ font: 700 0.75rem var(--font-mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent2); margin-bottom: 0.6rem; }}
    header.masthead h1 {{ font-family: var(--font-head); font-size: 2.4rem; font-weight: 700; line-height: 1.25; }}
    header.masthead .subtitle {{ font-family: var(--font-head); font-style: italic; font-size: 1.05rem; color: var(--muted); margin-top: 0.5rem; }}
    header.masthead .meta {{ font-size: 0.8rem; color: var(--muted); margin-top: 0.9rem; font-family: var(--font-mono); }}

    .series-bar {{
      display: flex; justify-content: space-between; align-items: center;
      gap: 12px; flex-wrap: wrap;
      font-family: var(--font); font-size: 0.8rem; color: var(--muted);
      border: 1px solid var(--rule); background: var(--bg2);
      border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 2rem;
    }}
    .series-bar .series-tag {{ font-family: var(--font-mono); font-weight: 700; letter-spacing: 0.08em; color: var(--accent); }}
    .series-bar a {{ color: var(--accent); text-decoration: none; margin-left: 1rem; }}
    .series-bar a:first-child {{ margin-left: 0; }}
    .series-bar a:hover {{ text-decoration: underline; }}

    .legacy {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 1.4rem; margin: 1.2rem 0; background: var(--bg2); border: 1px solid var(--rule); border-radius: 10px; padding: 1.1rem 1.2rem; }}
    .legacy .legacy-who {{ font-family: var(--font-mono); font-size: 0.78rem; color: var(--accent2); margin-bottom: 0.6rem; }}
    .legacy blockquote {{ font-family: var(--font-head); font-style: italic; font-size: 0.95rem; margin-bottom: 0.7rem; padding-left: 0.8rem; border-left: 3px solid var(--accent); }}
    .legacy blockquote cite {{ display: block; font-style: normal; font-size: 0.76rem; color: var(--muted); margin-top: 0.25rem; }}
    .legacy .legacy-title {{ font-weight: 700; font-size: 0.85rem; color: var(--accent); margin-bottom: 0.4rem; }}
    .legacy ul {{ margin: 0 0 0 1.1rem; font-size: 0.88rem; }}
    @media (max-width: 700px) {{ .legacy {{ grid-template-columns: 1fr; }} }}

    .history {{ background: var(--bg); border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0; padding: 0.9rem 1.1rem; margin: 1.2rem 0; font-size: 0.92rem; }}
    .history .history-title {{ display: block; font-family: var(--font-mono); font-weight: 700; font-size: 0.78rem; letter-spacing: 0.08em; color: var(--accent); margin-bottom: 0.35rem; }}
    .history p {{ margin-bottom: 0.55rem; }}
    .history p:last-child {{ margin-bottom: 0; }}

    section.sec {{ margin-bottom: 3.5rem; }}
    section.sec.hidden-by-search {{ display: none; }}
    h2 {{ font-family: var(--font-head); font-size: 1.5rem; font-weight: 700; padding-bottom: 0.5rem; border-bottom: 2px solid var(--accent); margin-bottom: 1.2rem; }}
    h2 .chapno {{ color: var(--accent2); font-family: var(--font-mono); font-size: 0.85rem; letter-spacing: 0.1em; display: block; margin-bottom: 0.3rem; }}
    h3 {{ font-family: var(--font-head); font-size: 1.1rem; font-weight: 700; margin: 1.6rem 0 0.6rem; }}
    p {{ margin-bottom: 0.9rem; font-size: 0.95rem; }}
    ul {{ margin: 0 0 1rem 1.3rem; font-size: 0.95rem; }}
    li {{ margin-bottom: 0.4rem; }}
    strong {{ color: var(--ink); }}
    p a, li a {{ color: var(--accent); }}

    .callout {{ border-left: 4px solid var(--accent2); background: var(--bg2); padding: 0.9rem 1.1rem; margin: 1.2rem 0; font-size: 0.92rem; border-radius: 0 8px 8px 0; }}
    .callout .callout-title {{ font-weight: 700; color: var(--accent2); display: block; margin-bottom: 0.3rem; font-size: 0.85rem; }}

    .diagram {{ margin: 1.6rem 0; background: var(--bg2); border: 1px solid var(--rule); border-radius: 10px; padding: 1.2rem; overflow-x: auto; }}
    .diagram figcaption {{ font-size: 0.85rem; font-weight: 700; color: var(--ink); margin-bottom: 0.8rem; }}
    .diagram pre.mermaid {{ text-align: center; }}

    .table-wrap {{ overflow-x: auto; overflow-y: auto; max-height: 600px; margin: 1.2rem 0; border: 1px solid var(--rule); border-radius: 10px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 0.88rem; }}
    th {{ background: var(--bg2); text-align: left; padding: 0.6rem 0.9rem; border-bottom: 2px solid var(--rule); font-weight: 700; white-space: nowrap; }}
    td {{ padding: 0.6rem 0.9rem; border-bottom: 1px solid var(--rule); vertical-align: top; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: var(--bg2); }}

    .formula {{
      font-family: var(--font-mono);
      background: var(--bg);
      border: 1px solid var(--rule);
      border-left: 4px solid var(--accent2);
      border-radius: 0 8px 8px 0;
      padding: 0.8rem 1rem;
      margin: 0.7rem 0;
      font-size: 0.95rem;
      overflow-x: auto;
    }}
    .formula .f-name {{ font-weight: 700; color: var(--accent); display: block; font-size: 0.78rem; letter-spacing: 0.04em; margin-bottom: 0.3rem; }}
    .formula .f-note {{ color: var(--muted); font-size: 0.8rem; display: block; margin-top: 0.3rem; }}

    footer {{ margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--rule); font-size: 0.8rem; color: var(--muted); font-family: var(--font-mono); }}

    @media (max-width: 900px) {{
      .shell {{ grid-template-columns: 1fr; }}
      .sidenav {{ position: static; max-height: none; }}
    }}
    @media print {{
      .sidenav {{ display: none; }}
      .shell {{ grid-template-columns: 1fr; }}
      section.sec {{ break-inside: avoid-page; }}
    }}
"""


def _strip_para(text):
    """去掉段落末尾多余的 </p>（数据中 intro 常以 </p> 结尾，渲染时再包一层 <p>）"""
    t = text.rstrip()
    if t.endswith("</p>"):
        t = t[:-4].rstrip()
    return t


def render_outline_keywords(ch):
    parts = []
    parts.append('        <h3>本章大纲</h3>')
    parts.append('        <ul>')
    for item in ch["outline"]:
        parts.append('          <li>%s</li>' % item)
    parts.append('        </ul>')
    parts.append('        <h3>核心知识点</h3>')
    parts.append('        <ul>')
    for item in ch["keywords"]:
        parts.append('          <li>%s</li>' % item)
    parts.append('        </ul>')
    return '\n'.join(parts)


def render_history(ch):
    parts = []
    parts.append('        <div class="history">')
    parts.append('          <span class="history-title">%s</span>' % ch.get("history_title", "历史背景"))
    for p in ch["history"]:
        parts.append('          <p>%s</p>' % p)
    parts.append('        </div>')
    return '\n'.join(parts)


def render_diagram(ch):
    parts = []
    parts.append('        <figure class="diagram">')
    parts.append('          <figcaption>%s</figcaption>' % ch["diagram_title"])
    parts.append('          <pre class="mermaid">')
    parts.append(ch["diagram"])
    parts.append('          </pre>')
    parts.append('        </figure>')
    return '\n'.join(parts)


def render_formulas(ch):
    parts = []
    parts.append('        <h3>公式速查：%s</h3>' % ch.get("formulas_title", "核心公式"))
    for name, content, note in ch["formulas"]:
        parts.append('        <div class="formula"><span class="f-name">%s</span>%s<span class="f-note">%s</span></div>' % (name, content, note))
    return '\n'.join(parts)


def render_table(ch):
    t = ch["table"]
    parts = []
    parts.append('        <h3>%s</h3>' % t["title"])
    parts.append('        <div class="table-wrap">')
    parts.append('          <table>')
    parts.append('            <thead>')
    parts.append('              <tr>' + ''.join('<th>%s</th>' % h for h in t["headers"]) + '</tr>')
    parts.append('            </thead>')
    parts.append('            <tbody>')
    for row in t["rows"]:
        parts.append('              <tr>' + ''.join('<td>%s</td>' % c for c in row) + '</tr>')
    parts.append('            </tbody>')
    parts.append('          </table>')
    parts.append('        </div>')
    return '\n'.join(parts)


def render_legacy(ch):
    parts = []
    parts.append('        <div class="legacy">')
    half = (len(ch["legacy"]) + 1) // 2
    col1 = ch["legacy"][:half]
    col2 = ch["legacy"][half:]
    for col in (col1, col2):
        parts.append('          <div>')
        for who, quote, cite in col:
            parts.append('            <div class="legacy-who">%s</div>' % who)
            parts.append('            <blockquote>%s<cite>——%s</cite></blockquote>' % (quote, cite))
        parts.append('          </div>')
    parts.append('        </div>')
    return '\n'.join(parts)


def render_chapter(ch):
    parts = []
    parts.append('      <section class="sec" id="%s">' % ch["id"])
    parts.append('        <h2><span class="chapno">%s</span>%s</h2>' % (ch["no"], ch["title"]))
    parts.append('        <p>%s</p>' % _strip_para(ch["intro"]))
    parts.append(render_outline_keywords(ch))
    if ch.get("summary"):
        parts.append(render_diagram(ch))
        parts.append(render_history(ch))
        if ch.get("table"):
            parts.append(render_table(ch))
        if ch.get("callout"):
            parts.append('        <div class="callout">')
            parts.append('          <span class="callout-title">%s</span>' % ch["callout_title"])
            parts.append('          %s' % ch["callout"])
            parts.append('        </div>')
    else:
        parts.append(render_history(ch))
        parts.append('        <h3>代表人物</h3>')
        for f in ch["figures"]:
            parts.append('        <p>%s</p>' % _strip_para(f))
        parts.append(render_diagram(ch))
        if ch.get("formulas"):
            parts.append(render_formulas(ch))
        if ch.get("table"):
            parts.append(render_table(ch))
        if ch.get("legacy"):
            parts.append(render_legacy(ch))
    parts.append('      </section>')
    return '\n'.join(parts)


def render_intro(v):
    parts = []
    parts.append('      <!-- 导言 -->')
    parts.append('      <section class="sec" id="intro">')
    parts.append('        <h2>%s</h2>' % v["intro_title"])
    parts.append('        <p>%s</p>' % _strip_para(v["intro_para"]))
    intro_ch = {
        "outline": v["intro_outline"],
        "keywords": v["intro_keywords"],
    }
    parts.append(render_outline_keywords(intro_ch))
    parts.append('        <div class="callout">')
    parts.append('          <span class="callout-title">一条主线</span>')
    parts.append('          %s' % v["intro_callout"])
    parts.append('        </div>')
    parts.append('        <p>%s</p>' % v["intro_para2"])
    labels = v["intro_map_labels"]
    nodes = []
    for i, lab in enumerate(labels):
        nodes.append('  %s["%s"]' % (chr(65 + i), lab))
    edges = []
    for i in range(len(labels) - 1):
        edges.append('  %s --> %s' % (chr(65 + i), chr(65 + i + 1)))
    mermaid = 'flowchart LR\n' + '\n'.join(nodes) + '\n' + '\n'.join(edges) + '\n  classDef shift fill:%s,color:#fff,stroke:%s;\n  class %s shift;' % (v["accent"], v["accent"], ','.join(chr(65 + i) for i in range(len(labels))))
    parts.append('        <figure class="diagram">')
    parts.append('          <figcaption>图 1 · %s</figcaption>' % v["intro_map_caption"])
    parts.append('          <pre class="mermaid">')
    parts.append(mermaid)
    parts.append('          </pre>')
    parts.append('        </figure>')
    parts.append('      </section>')
    return '\n'.join(parts)


def build_html(v, desktop=False):
    if desktop:
        index_href = "../index.html"
        prev_href = ("../%s/%s" % v["prev_dt"]) if v.get("prev_dt") else None
        next_href = ("../%s/%s" % v["next_dt"]) if v.get("next_dt") else None
    else:
        index_href = "../思想图谱系列/index.html"
        prev_href = ("../%s/%s" % v["prev_ws"]) if v.get("prev_ws") else None
        next_href = ("../%s/%s" % v["next_ws"]) if v.get("next_ws") else None

    # counts
    n_diagrams = 1 + len(v["chapters"])
    n_tables = sum(1 for c in v["chapters"] if c.get("table"))
    n_quotes = sum(len(c.get("legacy", [])) for c in v["chapters"])
    q_floor = max(10, (n_quotes // 10) * 10)

    # toc
    toc = []
    toc.append('      <li><a href="#intro">%s</a></li>' % v["intro_toc"])
    for c in v["chapters"]:
        toc.append('      <li><a href="#%s">%s · %s</a></li>' % (c["id"], c["no"], c["title"]))
    toc_html = '\n'.join(toc)

    # nav links
    nav_parts = []
    nav_parts.append('          <a href="%s">系列目录</a>' % index_href)
    if prev_href:
        nav_parts.append('          <a href="%s">← 上一辑 · %s</a>' % (prev_href, v["prev_name"]))
    if next_href:
        nav_parts.append('          <a href="%s">下一辑 · %s →</a>' % (next_href, v["next_name"]))
    nav_html = '\n'.join(nav_parts)

    # main content
    main_parts = []
    main_parts.append('    <main>')
    main_parts.append(render_intro(v))
    for c in v["chapters"]:
        main_parts.append(render_chapter(c))
    main_parts.append('    </main>')

    css_body = CSS_BODY.format(accent=v["accent"], accent2=v["accent2"])

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%s · 思想图谱系列%s</title>

  <style>
%s
  </style>

  <style>
%s
  </style>
</head>

<body>
<div class="shell">

  <nav class="sidenav" aria-label="目录">
    <div class="brand">%s</div>
    <div class="brand-sub">思想图谱系列 · %s</div>
    <input class="searchbox" id="searchInput" type="search" placeholder="搜索章节内容…" aria-label="搜索章节内容">
    <ul class="toc" id="toc">
%s
    </ul>
  </nav>

  <article class="page">
    <header class="masthead">
      <nav class="series-bar" aria-label="系列导航">
        <span class="series-tag">思想图谱系列 · %s</span>
        <span class="series-links">
%s
        </span>
      </nav>
      <div class="kicker">思想图谱系列</div>
      <h1>%s</h1>
      <p class="subtitle">%s</p>
      <p class="meta">作者：詹家杨 · 2026-09-05 · %d 张思维导图 · %d 张对照表 · %d+ 人物语录 · %s</p>
    </header>

%s

    <footer>
      %s · 思想图谱系列%s · 作者：詹家杨 · 由 Trae Work 生成 · 2026-09-05
    </footer>
  </article>
</div>

<script src="./_shared/js/mermaid.min.js"></script>
<script src="assets/main.js"></script>
</body>
</html>
""" % (
        v["title"], v["no_label"],
        CSS,
        css_body,
        v["brand"], v["no_label"],
        toc_html,
        v["no_label"],
        nav_html,
        v["title"],
        v["subtitle"],
        n_diagrams, n_tables, q_floor, v["tag"],
        '\n'.join(main_parts),
        v["title"], v["no_label"],
    )
    return html
