# -*- coding: utf-8 -*-
"""生成思想图谱系列阅读指南与目录"""
import os, re, json, shutil

BASE = r"C:\Users\Admin1\Documents\FastViewCloudService"

with open(os.path.join(BASE, "volumes_data.json"), "r", encoding="utf-8") as f:
    VOLUMES = json.load(f)

def get_stats(dir_name, file_name):
    path = os.path.join(BASE, dir_name, file_name)
    if not os.path.exists(path):
        alt = {"truth-dimensions":"truth-dimensions.html","series-overview":"series-overview.html",
               "eastern-thought-lineage":"eastern-thought-lineage.html","econ-part2-lineage":"econ-part2-lineage.html",
               "education-lineage":"education-lineage.html","art-aesthetics-lineage":"art-aesthetics-lineage.html",
               "life-science-lineage":"life-science-lineage.html","isms-lineage":"isms-lineage.html"}
        if dir_name in alt:
            path = os.path.join(BASE, dir_name, alt[dir_name])
    if not os.path.exists(path):
        return {"lines": 0, "mermaid": 0, "explain": 0, "tables": 0, "quotes": 0, "size": 0}
    with open(path, "r", encoding="utf-8") as fh:
        c = fh.read()
    return {"lines": len(c.split("\n")), "mermaid": len(re.findall(r'class="mermaid"', c)),
            "explain": len(re.findall(r'class="explain"', c)), "tables": len(re.findall(r'<table', c)),
            "quotes": len(re.findall(r'<blockquote', c)), "size": os.path.getsize(path)}

vol_stats = {}
for v in VOLUMES:
    stats = get_stats(v["dir"], v["file"])
    vol_stats[v["vol"]] = stats

tm = sum(s["mermaid"] for s in vol_stats.values())
te = sum(s["explain"] for s in vol_stats.values())
tt = sum(s["tables"] for s in vol_stats.values())
tq = sum(s["quotes"] for s in vol_stats.values())
tl = sum(s["lines"] for s in vol_stats.values())
ts = sum(s["size"] for s in vol_stats.values())

STAGE_COLORS = {"奠": "#3E4A78", "社": "#6A4C93", "物": "#4F7A28", "文": "#8C2F39", "未": "#6D28D9", "内": "#9E2A5B", "传": "#15803D", "收": "#7C2D12"}
STAGE_COLORS_VAR = {"奠": "var(--c1)", "社": "var(--c2)", "物": "var(--c3)", "文": "var(--c4)", "未": "var(--c5)", "内": "var(--c6)", "传": "var(--c7)", "收": "var(--c8)"}

def stage_num(tag):
    m = {"奠基":1,"社会":2,"物质":3,"文明":4,"未来":5,"内心":6,"传承":7,"收束":8}
    return m.get(tag, 0)

def gen_stage_block(stage_num, tag):
    names = {1:"奠基 \u00b7 如何思考",2:"社会 \u00b7 人与人的秩序",3:"物质 \u00b7 财富与自然",4:"文明 \u00b7 历史与力量",5:"未来 \u00b7 科技与智能",6:"内心 \u00b7 审美与心灵",7:"传承 \u00b7 文明延续",8:"收束 \u00b7 把一切收拢成一张图"}
    qs = {1:"先学会正确地想",2:"看清楚人与人",3:"看清楚人与物",4:"回望时间之内",5:"眺望时间之外",6:"回到人自身",7:"如何让这一切延续",8:"最后的回望"}
    descs = {
        1: '这一阶段是全卷的\u201c地基\u201d，回答一个元问题：我怎么知道自己想得对？在接触任何具体学问之前，必须先建立理性工具的可靠性。先读逻辑掌握推理的规则与极限，再读数学建立精确抽象的思维，然后建立东西方两大思想传统\u2014\u2014西方哲学与东方思想，最后用概念词典统一术语、用真理的多维图景回答\u201c什么是真\u201d；宗教学与神话则从神圣维度追问人类信仰的根源。',
        2: '掌握了思考工具之后，第一件要面对的现实就是人与人的关系。这一阶段是全书体量最大的一环，因为它回答的是我们每天都在经历却未必察觉的问题：秩序从哪里来？先读社会看抽象的\u201c社会\u201d如何运作，再读政治看具体的\u201c权力与秩序\u201d，国际关系把视野放到国家之间，人类学则把你带出去看\u201c他者\u201d、反思\u201c自身\u201d。随后进入左右两条西方政治长河\u2014\u2014马克思主义与自由主义；最后用法哲学的\u201c正义与规则\u201d和伦理的\u201c善与恶\u201d为这段旅程落下价值标尺。',
        3: '处理完人际关系，接着面对人与物质世界的关系：我们如何创造财富、又如何理解自然。先用经济看财富的古典脉络，再用经济下篇潜入当代深水区（增长、金融、平台、AI经济）；然后由科学总领世界观的重塑，落到生命科学与地理环境；物理学与天文学揭示宇宙的基本规律，化学连接物理与生命，医学与健康守护人的身体。',
        4: '看清了\u201c当下\u201d的人与物，还要知道\u201c当下\u201d是怎么来的。这一阶段把镜头拉高，回望时间的纵深与冲突的代价。先读历史理解人类如何记录、理解与运用过去；再读军事战略直面人类最极端的冲突与暴力，理解\u201c不战而胜、威慑和平\u201d的战略智慧。',
        5: '回望了来路，就轮到去路。这一阶段有两辑，是全书\u201c主航道\u201d\u2014\u2014科技与人工智能与计算机科学。从石器到AGI，串联六次技术跃迁，理解工具如何改造世界、又如何反过来重塑人。它既是前面\u201c科学\u201d的延伸，也是后面\u201c内心\u201d的引子\u2014\u2014因为AI最终迫使我们重新回答\u201c人是什么\u201d。',
        6: '外部世界走完一圈，最终要回到人如何感受、如何理解自己。这一阶段安顿的是感性、语言与心灵。先用艺术与美学追问\u201c美\u201d，再读心理学剖析\u201c心\u201d；文学与语言教你用语言创造意义，语言学揭示语言本身的科学规律，传播与媒介教你理解信息如何抵达人心，修辞与演说教你如何以言成事。这六辑共同构成一个\u201c内心世界\u201d的闭环。',
        7: '认识了自己，最后要问的是这一切如何传递下去。这一阶段的唯一主角是教育\u2014\u2014文明的\u201c元机制\u201d。从\u201c有教无类\u201d到\u201c终身学习\u201d，东方从孔子到书院、西方从苏格拉底到卢梭，提炼\u201c有教无类、因材施教、知行合一、教学相长、终身学习\u201d的教育规律，是整套系列的自我指涉与收束前奏。',
        8: '最后一辑（系列总览）不是新知，而是一张收拢全卷的大图谱。先看三十六辑全景与阅读路径，再逐阶段导读各自的骨架，最后用\u201c左、右、东\u201d三条思想长河的对照，把散落在各辑的内容收拢成一张可一眼看尽的图。',
    }
    vols = [v for v in VOLUMES if v["stage"] == stage_num]
    chips = "\n".join('          <span class="chip"><span class="n">%s</span> %s</span>' % (v["vol"].replace("VOL.",""), v["name"].replace("<br>"," ")) for v in vols)
    cards = []
    for v in vols:
        s = vol_stats.get(v["vol"], {})
        parts = []
        if s.get("mermaid",0): parts.append("%d \u5f20\u601d\u7ef4\u5bfc\u56fe" % s["mermaid"])
        if s.get("tables",0): parts.append("%d \u5f20\u5bf9\u7167\u8868" % s["tables"])
        if s.get("explain",0): parts.append("%d \u4e2a\u6df1\u5ea6\u89e3\u91ca\u5757" % s["explain"])
        if s.get("quotes",0): parts.append("%d \u6761\u4eba\u7269\u8bed\u5f55" % s["quotes"])
        st = " \u00b7 ".join(parts) if parts else "\u7ae0\u8282\u641c\u7d22"
        cards.append('    <a class="vol" href="../%s/%s">\n      <p class="vol-no">%s \u00b7 %s</p>\n      <h2>%s</h2>\n      <p class="vol-sub">%s</p>\n      <p class="vol-stats">%s</p>\n      <p class="vol-cta">\u6253\u5f00\u56fe\u8c31 \u2192</p>\n    </a>' % (v["dir"], v["file"], v["vol"], v["name"].replace("<br>"," "), v["name"], v["desc"], st))
    cards_html = "\n".join(cards)
    c = STAGE_COLORS[tag[:1]]
    return '''    <section class="stage-block" id="s%d" style="--ac: %s">
      <div class="stage-head"><span class="s-no">\u7b2c%d\u9636\u6bb5</span><span class="s-name">%s</span><span class="s-q">\u2014\u2014%s</span></div>
      <div class="stage-ac">
        <div class="stage-body"><p>%s</p></div>
        <div class="vols-inline">
%s
        </div>
      </div>
    </section>
    <div class="volumes">
%s
    </div>''' % (stage_num, c, stage_num, names[stage_num], qs[stage_num], descs[stage_num], chips, cards_html)

def gen_table():
    rows = []
    for v in VOLUMES:
        c = STAGE_COLORS_VAR[v["tag"][:1]]
        rows.append('          <tr><td class="vol-no">%s</td><td class="vol-name">%s</td><td>%s</td><td class="vol-stage"><span class="dot" style="background:%s"></span>%s</td></tr>' % (v["vol"], v["name"].replace("<br>"," "), v["core"], c, v["tag"]))
    return "\n".join(rows)

# 读取CSS模板
CSS = open(os.path.join(BASE, "_gen_reading_guide.py"), "r", encoding="utf-8").read()
# 直接用内联CSS

print("数据采集完成:")
print("  36卷, %d行, %d思维导图, %d解释块, %d对照表, %d引用" % (tl, tm, te, tt, tq))

# 构建HTML - 分段写入避免format问题
parts = []
parts.append('''<!-- Generated by Trae Work -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u601d\u60f3\u56fe\u8c31\u7cfb\u5217 \u00b7 \u9605\u8bfb\u6307\u5357\u4e0e\u76ee\u5f55</title>
<style>
@font-face { font-family: "CrimsonPro"; src: url("../isms-glossary/_shared/fonts/CrimsonPro-Regular.ttf") format("truetype"); font-weight: 400; }
@font-face { font-family: "CrimsonPro"; src: url("../isms-glossary/_shared/fonts/CrimsonPro-Bold.ttf") format("truetype"); font-weight: 700; }
@font-face { font-family: "InstrumentSans"; src: url("../isms-glossary/_shared/fonts/InstrumentSans-Regular.ttf") format("truetype"); font-weight: 400; }
@font-face { font-family: "InstrumentSans"; src: url("../isms-glossary/_shared/fonts/InstrumentSans-Bold.ttf") format("truetype"); font-weight: 700; }
@font-face { font-family: "JetBrainsMono"; src: url("../isms-glossary/_shared/fonts/JetBrainsMono-Regular.ttf") format("truetype"); font-weight: 400; }
:root { --bg: #FAF8F3; --bg2: #F1EDE4; --ink: #26221B; --muted: #6E6759; --rule: #E2DCCE; --c1: #3E4A78; --c2: #6A4C93; --c3: #4F7A28; --c4: #8C2F39; --c5: #6D28D9; --c6: #9E2A5B; --c7: #15803D; --c8: #7C2D12; --gold: #A67C2E; --font-serif: "CrimsonPro", "Songti SC", "STSong", "SimSun", serif; --font-sans: "InstrumentSans", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif; --font-mono: "JetBrainsMono", Consolas, monospace; }
html { scroll-behavior: smooth; }
body { font-family: var(--font-sans); color: var(--ink); background: var(--bg); line-height: 1.75; }
* { box-sizing: border-box; margin: 0; padding: 0; }
.shell { display: grid; grid-template-columns: 264px minmax(0, 1fr); gap: 3rem; max-width: 1220px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
.sidenav { position: sticky; top: 2rem; align-self: start; max-height: calc(100vh - 4rem); overflow-y: auto; padding-right: 0.5rem; }
.sidenav .brand { font-family: var(--font-serif); font-size: 1.06rem; font-weight: 700; margin-bottom: 0.25rem; }
.sidenav .brand-sub { font-size: 0.76rem; color: var(--muted); margin-bottom: 1.1rem; }
.toc { list-style: none; font-size: 0.84rem; }
.toc li { margin-bottom: 0.1rem; }
.toc a { display: block; padding: 0.34rem 0.55rem; color: var(--muted); text-decoration: none; border-left: 2px solid var(--rule); }
.toc a:hover, .toc a.active { color: var(--gold); border-left-color: var(--gold); background: var(--bg2); }
article { min-width: 0; }
.masthead { border-bottom: 2px solid var(--ink); padding-bottom: 1.6rem; margin-bottom: 2.4rem; }
.kicker { font-family: var(--font-mono); font-size: 13px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold); margin-bottom: 14px; }
.masthead h1 { font-family: var(--font-serif); font-weight: 700; font-size: 46px; line-height: 1.14; margin-bottom: 14px; }
.masthead .lede { font-family: var(--font-serif); font-style: italic; font-size: 1.06rem; color: var(--muted); margin-bottom: 10px; }
.masthead .author { font-size: 0.85rem; color: var(--gold); }
.lead { font-size: 1.02rem; } .lead p { margin-bottom: 1rem; }
strong { color: var(--ink); font-weight: 700; }
h2.sec-head { font-family: var(--font-serif); font-size: 1.7rem; font-weight: 700; padding-top: 2.6rem; margin-top: 2.6rem; margin-bottom: 1.2rem; border-top: 2px solid var(--ink); scroll-margin-top: 1rem; }
h2.sec-head .no { font-family: var(--font-mono); color: var(--gold); font-size: 0.95rem; font-weight: 400; margin-right: 0.4rem; letter-spacing: 0.05em; }
h3 { font-family: var(--font-serif); font-size: 1.22rem; font-weight: 700; margin: 1.8rem 0 0.7rem; }
.intro-card { border: 1px solid var(--rule); background: var(--bg2); border-radius: 12px; padding: 24px 28px; margin: 1.4rem 0; }
.intro-card h3 { margin-top: 0; } .intro-card p { font-size: 0.95rem; margin-bottom: 0.6rem; } .intro-card p:last-child { margin-bottom: 0; }
.table-wrap { overflow-x: auto; overflow-y: auto; max-height: 620px; margin: 1rem 0 2rem; border: 1px solid var(--rule); border-radius: 10px; background: #fff; }
table { width: 100%; border-collapse: collapse; font-size: 0.85rem; min-width: 720px; }
thead th { position: sticky; top: 0; background: var(--bg2); font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; text-align: left; padding: 0.7rem 0.9rem; border-bottom: 2px solid var(--rule); white-space: nowrap; }
tbody td { padding: 0.62rem 0.9rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
tbody tr:last-child td { border-bottom: none; } tbody tr:hover { background: #FBf7ef; }
td.vol-no { font-family: var(--font-mono); font-size: 0.76rem; color: var(--muted); white-space: nowrap; } td.vol-name { font-weight: 700; white-space: nowrap; } td.vol-stage { white-space: nowrap; }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.stage-block { margin: 2.2rem 0 2.6rem; }
.stage-head { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; border-bottom: 1px solid var(--rule); padding-bottom: 0.5rem; margin-bottom: 0.9rem; }
.stage-head .s-no { font-family: var(--font-mono); font-size: 0.8rem; letter-spacing: 0.12em; color: var(--ac); }
.stage-head .s-name { font-family: var(--font-serif); font-size: 1.4rem; font-weight: 700; }
.stage-head .s-q { font-size: 0.85rem; color: var(--muted); }
.stage-ac { border-left: 4px solid var(--ac); margin-left: 0.4rem; }
.stage-body p { font-size: 0.95rem; margin-bottom: 0.7rem; }
.vols-inline { margin: 0.6rem 0 1rem; }
.vols-inline .chip { display: inline-block; font-family: var(--font-mono); font-size: 0.76rem; background: var(--bg2); border: 1px solid var(--rule); border-radius: 999px; padding: 0.2rem 0.7rem; margin: 0.2rem 0.3rem 0.2rem 0; color: var(--ink); }
.vols-inline .chip .n { color: var(--muted); }
.volumes { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-bottom: 48px; }
.vol { display: flex; flex-direction: column; background: var(--bg2); border: 1px solid var(--rule); border-radius: 12px; padding: 28px; text-decoration: none; color: var(--ink); transition: transform 0.15s ease, box-shadow 0.15s ease; }
.vol:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(38, 34, 27, 0.10); }
.vol .vol-no { font-family: var(--font-mono); font-size: 12px; letter-spacing: 0.12em; margin-bottom: 14px; }
.vol h2 { font-family: var(--font-serif); font-size: 24px; font-weight: 700; line-height: 1.3; margin-bottom: 8px; }
.vol .vol-sub { font-size: 14px; color: var(--muted); margin-bottom: 16px; flex: 1; }
.vol .vol-stats { font-family: var(--font-mono); font-size: 12px; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 12px; margin-bottom: 14px; }
.vol .vol-cta { font-size: 14px; font-weight: 700; }
.path-card { border: 1px solid var(--rule); border-radius: 12px; background: #fff; padding: 22px 26px; margin: 1.2rem 0; }
.path-card h3 { margin-top: 0; display: flex; align-items: center; gap: 10px; }
.path-card .tag { font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.08em; color: #fff; background: var(--ac); border-radius: 4px; padding: 2px 8px; text-transform: uppercase; }
.path-card ol { padding-left: 1.2rem; margin: 0.7rem 0; }
.path-card li { font-size: 0.92rem; margin-bottom: 0.4rem; }
.path-card p { font-size: 0.92rem; color: var(--muted); }
.method-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 1.2rem 0 2rem; }
.method { border: 1px solid var(--rule); border-radius: 10px; background: var(--bg2); padding: 18px 20px; }
.method h4 { font-family: var(--font-serif); font-size: 1.02rem; font-weight: 700; margin-bottom: 0.5rem; }
.method p { font-size: 0.88rem; color: var(--muted); }
.closing { border-left: 4px solid var(--gold); background: var(--bg2); border-radius: 0 10px 10px 0; padding: 22px 26px; margin-top: 2.4rem; }
.closing p { font-family: var(--font-serif); font-size: 1.05rem; line-height: 1.9; }
.closing .sig { display: block; margin-top: 1rem; font-family: var(--font-mono); font-size: 0.8rem; color: var(--muted); }
.inline-toc { border: 1px solid var(--rule); background: var(--bg2); border-radius: 10px; padding: 18px 22px; margin: 1.8rem 0 2.2rem; }
.inline-toc-head { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold); margin-bottom: 0.5rem; }
.inline-toc-links { display: flex; flex-wrap: wrap; gap: 0.4rem 1.2rem; }
.inline-toc-links a { font-size: 0.88rem; color: var(--muted); text-decoration: none; padding: 0.2rem 0; border-bottom: 1px solid transparent; }
.inline-toc-links a:hover { color: var(--gold); border-bottom-color: var(--gold); }
footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--rule); font-family: var(--font-mono); font-size: 0.76rem; color: var(--muted); }
@media (max-width: 900px) { .shell { grid-template-columns: 1fr; } .sidenav { position: static; max-height: none; border-bottom: 1px solid var(--rule); padding-bottom: 1rem; margin-bottom: 1rem; overflow: visible; } .toc { columns: 2; } .masthead h1 { font-size: 34px; } }
@media (max-width: 560px) { .toc { columns: 1; } body { font-size: 15px; } }
@media print { .sidenav { display: none; } .shell { grid-template-columns: 1fr; } .table-wrap { max-height: none; } }
</style>
</head>
<body>
<div class="shell">
  <nav class="sidenav">
    <div class="brand">\u601d\u60f3\u56fe\u8c31\u7cfb\u5217</div>
    <div class="brand-sub">\u9605\u8bfb\u6307\u5357\u4e0e\u76ee\u5f55</div>
    <ul class="toc" id="toc">
      <li><a href="#overview">01 \u00b7 \u7cfb\u5217\u603b\u89c8</a></li>
      <li><a href="#map">02 \u00b7 \u4e09\u5341\u516d\u8f91\u5168\u89c8</a></li>
      <li><a href="#stages">03 \u00b7 \u516b\u9636\u6bb5\u5212\u5206</a></li>
      <li><a href="#paths">04 \u00b7 \u9605\u8bfb\u8def\u5f84\u5efa\u8bae</a></li>
      <li><a href="#method">05 \u00b7 \u5982\u4f55\u8bfb\u6bcf\u4e00\u8f91</a></li>
      <li><a href="#closing">\u7ed3\u8bed</a></li>
      <li style="margin-top:0.8rem;border-top:1px solid var(--rule);padding-top:0.8rem;"><a href="./\u4e3b\u9898\u7d22\u5f15.html">\u4e3b\u9898\u7d22\u5f15 \u2192</a></li>
    </ul>
  </nav>
  <article>
    <header class="masthead">
      <p class="kicker">Reading Guide \u00b7 \u603b\u5bfc\u8bfb</p>
      <h1>\u601d\u60f3\u56fe\u8c31\u7cfb\u5217<br>\u9605\u8bfb\u6307\u5357\u4e0e\u9636\u6bb5\u5212\u5206</h1>
      <p class="lede">\u4e00\u5957\u6309\u201c\u5960\u57fa \u2192 \u793e\u4f1a \u2192 \u7269\u8d28 \u2192 \u6587\u660e \u2192 \u672a\u6765 \u2192 \u5185\u5fc3 \u2192 \u4f20\u627f \u2192 \u603b\u89c8\u201d\u516b\u9636\u9012\u8fdb\u7684\u901a\u8bc6\u6559\u80b2\u7cfb\u7edf</p>
      <p class="author">\u539f\u521b\u4f5c\u8005\uff1a\u8a79\u5bb6\u6768\u3001\u8fdf\u541b\u8fbe</p>
    </header>
    <div class="lead">
      <p>\u300a\u601d\u60f3\u56fe\u8c31\u7cfb\u5217\u300b\u662f\u4e00\u5957\u8986\u76d6<strong>\u4e09\u5341\u516d\u5929\u4e3b\u9898</strong>\u7684<strong>\u901a\u8bc6\u6559\u80b2\u77e5\u8bc6\u56fe\u8c31</strong>\u2014\u2014\u4e0d\u4e3a\u5e94\u8bd5\uff0c\u4e5f\u4e0d\u4e3a\u804c\u4e1a\u901f\u6210\uff0c\u800c\u662f\u56de\u5230\u201c\u4eba\u5982\u4f55\u8ba4\u8bc6\u4e16\u754c\u3001\u53c8\u5982\u4f55\u5b89\u987f\u81ea\u5df1\u201d\u8fd9\u4e00\u6839\u672c\u95ee\u9898\uff0c\u628a\u6563\u843d\u7684\u6982\u5ff5\u3001\u4e3b\u4e49\u4e0e\u601d\u60f3\u8fde\u6210\u4e00\u6761\u53ef\u4ee5\u6765\u56de\u7ffb\u9605\u7684\u8109\u7edc\u3002</p>
      <p>\u901a\u8bc6\u6559\u80b2\uff08Liberal Arts\uff09\u7684\u8981\u4e49\uff0c\u4ece\u6765\u4e0d\u662f\u8bb0\u4f4f\u66f4\u591a\u540d\u8bcd\uff0c\u800c\u662f\u6536\u83b7\u4e00\u79cd<strong>\u8de8\u754c\u7684\u5224\u65ad\u529b</strong>\uff1a\u5f53\u4f60\u5728\u65b0\u95fb\u91cc\u8bfb\u5230\u201c\u81ea\u7531\u4e3b\u4e49\u201d\u3001\u5728\u8bfe\u5802\u4e0a\u9047\u5230\u201c\u5269\u4f59\u4ef7\u503c\u201d\u3001\u5728\u8ba8\u8bba\u4e2d\u8c08\u5230\u201c\u4ec1\u653f\u201d\u65f6\uff0c\u80fd\u7acb\u523b\u660e\u767d\u5b83\u4eec\u80cc\u540e\u7ad9\u7740\u600e\u6837\u7684\u8c31\u7cfb\u3001\u5728\u56de\u7b54\u4ec0\u4e48\u95ee\u9898\u3001\u53c8\u4e0e\u54ea\u4e9b\u7acb\u573a\u76f8\u5bf9\u7167\u3002</p>
      <p>\u4e09\u5341\u516d\u8f91\u4e0d\u662f\u4e09\u5341\u516d\u672c\u5f7c\u6b64\u5b64\u7acb\u7684\u5c0f\u518c\u5b50\uff0c\u800c\u662f\u4e00\u4e2a<strong>\u6709\u6b21\u5e8f\u3001\u6709\u5c42\u7ea7\u3001\u6709\u547c\u5e94</strong>\u7684\u6574\u4f53\u3002\u8fd9\u4efd\u6307\u5357\u8981\u505a\u7684\uff0c\u5c31\u662f\u628a\u8fd9\u4e2a\u6574\u4f53\u62c6\u5f00\u8bb2\u6e05\u695a\uff1a\u6bcf\u4e00\u8f91\u7684\u4f4d\u7f6e\u3001\u6bcf\u9636\u6bb5\u7684\u95ee\u9898\u3001\u4ee5\u53ca\u4f60\u8be5\u6309\u4ec0\u4e48\u987a\u5e8f\u3001\u7528\u4ec0\u4e48\u65b9\u6cd5\u53bb\u8bfb\u5b83\u3002</p>
    </div>
    <div class="inline-toc">
      <div class="inline-toc-head">\u672c\u6307\u5357\u7ae0\u8282</div>
      <div class="inline-toc-links">
        <a href="#overview">01\u00b7\u7cfb\u5217\u603b\u89c8</a>
        <a href="#map">02\u00b7\u4e09\u5341\u516d\u8f91\u5168\u89c8</a>
        <a href="#stages">03\u00b7\u516b\u9636\u6bb5\u5212\u5206</a>
        <a href="#paths">04\u00b7\u9605\u8bfb\u8def\u5f84\u5efa\u8bae</a>
        <a href="#method">05\u00b7\u5982\u4f55\u8bfb\u6bcf\u4e00\u8f91</a>
        <a href="#closing">\u7ed3\u8bed</a>
      </div>
    </div>
''')

# 01 系列总览
parts.append('''    <h2 class="sec-head" id="overview"><span class="no">01</span>\u7cfb\u5217\u603b\u89c8</h2>
    <p><strong>\u4e00\u53e5\u8bdd\u5b9a\u4f4d\uff1a</strong>\u8fd9\u662f\u4e3a\u201c\u60f3\u8981\u63a5\u53d7\u901a\u8bc6\u6559\u80b2\u7684\u5b66\u4e60\u8005\u201d\u6253\u9020\u7684<strong>\u4e09\u5341\u516d\u4efd\u53ef\u68c0\u7d22\u3001\u53ef\u5bf9\u7167\u3001\u53ef\u56fe\u6848\u5316</strong>\u7684\u601d\u60f3\u56fe\u8c31\uff0c\u8986\u76d6\u4ece\u903b\u8f91\u3001\u54f2\u5b66\u3001\u653f\u6cbb\u3001\u7ecf\u6d4e\u3001\u79d1\u5b66\u5230\u827a\u672f\u3001\u6587\u5b66\u3001\u5fc3\u7406\u5b66\u3001\u6559\u80b2\u7684\u4eba\u6587\u5b66\u79d1\u4e0e\u81ea\u7136\u79d1\u5b66\u6838\u5fc3\u7248\u56fe\u3002</p>
    <p><strong>\u7edf\u4e00\u5f62\u6001\uff1a</strong>\u6bcf\u4e00\u8f91\u90fd\u9075\u5faa\u540c\u4e00\u5957\u7ed3\u6784\u2014\u2014\u4e00\u4e2a\u603b\u7eb2\uff08\u5bfc\u8a00\uff09\u3001\u82e5\u5e72\u7ae0\u8282\u3001\u6bcf\u7ae0\u4e00\u5f20<strong>\u601d\u7ef4\u5bfc\u56fe</strong>\u3001\u82e5\u5e72<strong>\u5bf9\u7167\u8868</strong>\u3001\u4e00\u6279<strong>\u4ee3\u8868\u4eba\u7269\u8bed\u5f55</strong>\u4e0e\u5386\u53f2\u80cc\u666f\u3002\u5728\u5168\u9762\u5347\u7ea7\u540e\uff0c\u6838\u5fc3\u8f91\u76ee\u5df2\u65b0\u589e<strong>\u57fa\u7840\u6982\u5ff5\u6811\u72b6\u56fe</strong>\u3001<strong>\u6269\u5c55\u6a21\u578b\u56fe</strong>\u4e0e<strong>\u6df1\u5ea6\u89e3\u91ca\u5757</strong>\uff08\u542b\u73b0\u5b9e\u6848\u4f8b\uff09\uff0c\u6bcf\u5377\u5e73\u5747\u589e\u52a0 300-600 \u884c\u8be6\u8ff0\u5185\u5bb9\u3002\u56e0\u6b64\u4e09\u5341\u516d\u8f91\u4e4b\u95f4\u201c\u683c\u5f0f\u7edf\u4e00\u3001\u53e3\u5f84\u4e00\u81f4\u201d\uff0c\u53ef\u4ee5\u6a2a\u5411\u5bf9\u7167\u7740\u8bfb\u3002</p>
    <div class="intro-card">
      <h3>\u4e09\u5927\u8bbe\u8ba1\u539f\u5219</h3>
      <p><strong>\u2460 \u8c31\u7cfb\u800c\u975e\u540d\u8bcd\u3002</strong>\u4e0d\u8bb2\u5b64\u7acb\u7684\u77e5\u8bc6\u70b9\uff0c\u4e13\u8bb2\u201c\u601d\u60f3\u7684\u6765\u9f99\u53bb\u8109\u201d\u3002</p>
      <p><strong>\u2461 \u5bf9\u7167\u800c\u975e\u72ec\u65ad\u3002</strong>\u6bcf\u8f91\u90fd\u914d\u6709\u5bf9\u7167\u8868\uff0c\u628a\u5bf9\u7acb\u7acb\u573a\u5e76\u6392\u6446\u51fa\u6765\uff0c\u8ba9\u8bfb\u8005\u81ea\u5df1\u770b\u3001\u81ea\u5df1\u5224\u65ad\u3002</p>
      <p><strong>\u2462 \u9012\u8fdb\u800c\u975e\u5e73\u94fa\u3002</strong>\u4e09\u5341\u516d\u8f91\u6309\u201c\u5982\u4f55\u601d\u8003 \u2192 \u4eba\u4e0e\u4eba\u7684\u79e9\u5e8f \u2192 \u8d22\u5bcc\u4e0e\u81ea\u7136 \u2192 \u6587\u660e\u4e0e\u5386\u53f2 \u2192 \u672a\u6765 \u2192 \u5185\u5fc3 \u2192 \u4f20\u627f\u201d\u5c42\u5c42\u9012\u8fdb\uff0c\u6700\u540e\u7528\u603b\u89c8\u6536\u62e2\u6210\u4e00\u5f20\u5927\u56fe\u3002</p>
    </div>
    <div class="intro-card" style="margin-top: 1rem;">
      <h3>\u5168\u7cfb\u5217\u6570\u636e\u603b\u89c8</h3>
      <p>\u5171 <strong>''' + str(len(VOLUMES)) + ''' \u5377</strong> \u00b7 <strong>''' + str(tm) + ''' \u5f20\u601d\u7ef4\u5bfc\u56fe</strong> \u00b7 <strong>''' + str(te) + ''' \u4e2a\u6df1\u5ea6\u89e3\u91ca\u5757</strong> \u00b7 <strong>''' + str(tt) + ''' \u5f20\u5bf9\u7167\u8868</strong> \u00b7 <strong>''' + str(tq) + ''' \u6761\u4eba\u7269\u8bed\u5f55</strong></p>
      <p>\u603b\u7bc7\u5e45 ''' + str(tl) + ''' \u884c \u00b7 ''' + "{:.2f}".format(ts/1024/1024) + ''' MB\uff08\u7eaf HTML\uff0c\u4e0d\u542b\u5916\u90e8\u8d44\u6e90\uff09</p>
    </div>
''')

# 02 三十六辑全览
parts.append('''    <h2 class="sec-head" id="map"><span class="no">02</span>\u4e09\u5341\u516d\u8f91\u5168\u89c8</h2>
    <p>\u4e0b\u8868\u6309<strong>\u8f91\u53f7\u987a\u5e8f</strong>\u5217\u51fa\u5168\u90e8\u4e09\u5341\u516d\u8f91\uff1b\u53f3\u4fa7\u201c\u9636\u6bb5\u201d\u4e00\u680f\u6807\u51fa\u5b83\u5728\u516b\u9636\u7ed3\u6784\u4e2d\u7684\u5f52\u5c5e\u3002\u8f91\u53f7\u662f\u521b\u4f5c\u5e8f\u53f7\uff0c\u9636\u6bb5\u662f\u9605\u8bfb\u6b21\u5e8f\u2014\u2014\u4e24\u8005\u5e76\u4e0d\u76f8\u540c\uff0c\u8fd9\u662f\u672c\u7cfb\u5217\u7684\u4e00\u4e2a\u5173\u952e\u8bbe\u8ba1\uff1a<strong>\u7528\u5e8f\u53f7\u6807\u660e\u8c31\u7cfb\u7684\u6df1\u6d45\uff0c\u7528\u9636\u6bb5\u6807\u660e\u9605\u8bfb\u7684\u5148\u540e</strong>\u3002</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>\u8f91\u53f7</th><th>\u8f91\u540d</th><th>\u6838\u5fc3\u4e4b\u95ee</th><th>\u6240\u5c5e\u9636\u6bb5</th></tr></thead>
        <tbody>
''' + gen_table() + '''
        </tbody>
      </table>
    </div>
''')

# 03 八阶段划分
parts.append('''    <h2 class="sec-head" id="stages"><span class="no">03</span>\u516b\u9636\u6bb5\u5212\u5206\u8be6\u89e3</h2>
    <p>\u5168\u4e66\u7684\u7ed3\u6784\uff0c\u662f\u4e00\u9053\u4ece<strong>\u201c\u5982\u4f55\u601d\u8003\u201d</strong>\u51fa\u53d1\u3001\u6700\u7ec8<strong>\u201c\u5b89\u987f\u81ea\u5df1\u3001\u4f20\u627f\u6587\u660e\u201d</strong>\u7684\u9012\u8fdb\u5f27\u7ebf\u3002\u5b83\u4e0d\u662f\u6309\u5b66\u79d1\u5206\u7c7b\uff0c\u800c\u662f\u6309<strong>\u4eba\u8ba4\u8bc6\u4e16\u754c\u7684\u903b\u8f91\u5c42\u6b21</strong>\u7ec4\u7ec7\u3002</p>
''')
for s in range(1, 9):
    tag = [v["tag"] for v in VOLUMES if v["stage"] == s][0]
    parts.append(gen_stage_block(s, tag))

# 04 阅读路径
parts.append('''    <h2 class="sec-head" id="paths"><span class="no">04</span>\u9605\u8bfb\u8def\u5f84\u5efa\u8bae</h2>
    <p>\u4e09\u5341\u516d\u8f91\u4e0d\u5fc5\u4e00\u6b21\u8bfb\u5b8c\uff0c\u66f4\u4e0d\u5fc5\u6309\u521b\u4f5c\u5e8f\u53f7\u8bfb\u3002\u4e0b\u9762\u7ed9\u51fa\u56db\u6761\u8def\u5f84\uff0c\u6309\u4f60\u7684\u76ee\u6807\u4e0e\u65f6\u95f4\u9009\u4e00\u6761\u5373\u53ef\u3002</p>
    <div class="path-card" style="--ac: var(--c8)">
      <h3><span class="tag">\u4e3b\u8def\u5f84</span>\u5faa\u5e8f\u6e10\u8fdb \u00b7 \u5b8c\u6574\u901a\u8bfb</h3>
      <p>\u9002\u5408\u60f3\u5b8c\u6574\u63a5\u53d7\u901a\u8bc6\u6559\u80b2\u7684\u5b66\u4e60\u8005\u3002</p>
      <ol>
        <li><strong>\u5960\u57fa</strong>\uff1a\u903b\u8f91 \u2192 \u6570\u5b66 \u2192 \u897f\u65b9\u54f2\u5b66 \u2192 \u4e1c\u65b9\u601d\u60f3 \u2192 \u6982\u5ff5\u8bcd\u5178 \u2192 \u771f\u7406\u591a\u7ef4 \u2192 \u5b97\u6559\u5b66\u4e0e\u795e\u8bdd</li>
        <li><strong>\u793e\u4f1a</strong>\uff1a\u793e\u4f1a \u2192 \u653f\u6cbb\u5b66\u901a\u8bba \u2192 \u56fd\u9645\u5173\u7cfb \u2192 \u4eba\u7c7b\u5b66 \u2192 \u9a6c\u514b\u601d\u4e3b\u4e49 \u2192 \u81ea\u7531\u4e3b\u4e49 \u2192 \u6cd5\u54f2\u5b66 \u2192 \u4f26\u7406</li>
        <li><strong>\u7269\u8d28</strong>\uff1a\u7ecf\u6d4e\u4e0a\u7bc7 \u2192 \u7ecf\u6d4e\u4e0b\u7bc7 \u2192 \u79d1\u5b66 \u2192 \u751f\u547d\u79d1\u5b66 \u2192 \u5730\u7406\u4e0e\u73af\u5883 \u2192 \u7269\u7406\u5b66 \u2192 \u5929\u6587\u5b66\u4e0e\u5b87\u5b99\u5b66 \u2192 \u5316\u5b66 \u2192 \u533b\u5b66\u4e0e\u5065\u5eb7</li>
        <li><strong>\u6587\u660e</strong>\uff1a\u5386\u53f2 \u2192 \u519b\u4e8b\u4e0e\u6218\u7565</li>
        <li><strong>\u672a\u6765</strong>\uff1a\u79d1\u6280\u4e0e\u4eba\u5de5\u667a\u80fd \u2192 \u8ba1\u7b97\u673a\u79d1\u5b66</li>
        <li><strong>\u5185\u5fc3</strong>\uff1a\u827a\u672f\u4e0e\u7f8e\u5b66 \u2192 \u5fc3\u7406\u5b66 \u2192 \u6587\u5b66\u4e0e\u8bed\u8a00 \u2192 \u8bed\u8a00\u5b66 \u2192 \u4f20\u64ad\u4e0e\u5a92\u4ecb \u2192 \u4fee\u8f9e\u4e0e\u6f14\u8bf4</li>
        <li><strong>\u4f20\u627f</strong>\uff1a\u6559\u80b2</li>
        <li><strong>\u6536\u675f</strong>\uff1a\u7cfb\u5217\u603b\u89c8\uff08\u8bfb\u5b8c\u56de\u6765\u770b\u4e00\u904d\uff09</li>
      </ol>
    </div>
    <div class="path-card" style="--ac: var(--c1)">
      <h3><span class="tag">\u901f\u6210\u8def\u5f84</span>\u6838\u5fc3\u4e5d\u8f91 \u00b7 \u5efa\u7acb\u9aa8\u67b6</h3>
      <p>\u9002\u5408\u65f6\u95f4\u6709\u9650\u3001\u60f3\u5148\u6293\u4e3b\u5e72\u7684\u8bfb\u8005\u3002</p>
      <ol>
        <li>\u903b\u8f91\u4e0e\u8bba\u8bc1\uff08VOL.20\uff09</li>
        <li>\u653f\u6cbb\u5b66\u901a\u8bba\uff08VOL.23\uff09</li>
        <li>\u7ecf\u6d4e\u601d\u60f3\u8c31\u7cfb\uff08VOL.07\uff09</li>
        <li>\u79d1\u5b66\u601d\u60f3\u8c31\u7cfb\uff08VOL.08\uff09</li>
        <li>\u7269\u7406\u5b66\u601d\u60f3\u8c31\u7cfb\uff08VOL.30\uff09</li>
        <li>\u79d1\u6280\u4e0e\u4eba\u5de5\u667a\u80fd\uff08VOL.12\uff09</li>
        <li>\u5fc3\u7406\u5b66\uff08VOL.18\uff09</li>
        <li>\u6559\u80b2\uff08VOL.19\uff09</li>
        <li>\u7cfb\u5217\u603b\u89c8\uff08VOL.06\uff09</li>
      </ol>
    </div>
    <div class="path-card" style="--ac: var(--c6)">
      <h3><span class="tag">\u4e13\u9898\u8def\u5f84</span>\u6309\u5174\u8da3\u5207\u5165</h3>
      <p>\u9002\u5408\u5e26\u7740\u5177\u4f53\u95ee\u9898\u6765\u7684\u8bfb\u8005\u3002</p>
      <ol>
        <li>\u5173\u5fc3<strong>\u653f\u6cbb\u4e0e\u4e3b\u4e49</strong> \u2192 \u4ece\u6982\u5ff5\u8bcd\u5178\u6216\u9a6c\u514b\u601d\u4e3b\u4e49/\u81ea\u7531\u4e3b\u4e49\u8fdb\u5165</li>
        <li>\u5173\u5fc3<strong>AI \u4e0e\u672a\u6765</strong> \u2192 \u4ece\u79d1\u6280\u4e0e\u4eba\u5de5\u667a\u80fd\u8fdb\u5165</li>
        <li>\u5173\u5fc3<strong>\u5185\u5fc3\u4e0e\u8868\u8fbe</strong> \u2192 \u4ece\u5fc3\u7406\u5b66\u6216\u6587\u5b66\u8fdb\u5165</li>
        <li>\u5173\u5fc3<strong>\u4eba\u4e0e\u81ea\u7136</strong> \u2192 \u4ece\u751f\u547d\u79d1\u5b66\u6216\u5730\u7406\u73af\u5883\u8fdb\u5165</li>
      </ol>
    </div>
    <div class="path-card" style="--ac: var(--c2)">
      <h3><span class="tag">\u5bf9\u7167\u8def\u5f84</span>\u6a2a\u5411\u6bd4\u8f83</h3>
      <p>\u9002\u5408\u5df2\u7ecf\u901a\u8bfb\u3001\u60f3\u52a0\u6df1\u7406\u89e3\u7684\u8bfb\u8005\u3002</p>
      <ol>
        <li>\u897f\u65b9\u54f2\u5b66 \u2194 \u4e1c\u65b9\u601d\u60f3</li>
        <li>\u9a6c\u514b\u601d\u4e3b\u4e49 \u2194 \u81ea\u7531\u4e3b\u4e49</li>
        <li>\u6cd5\u54f2\u5b66 \u2194 \u4f26\u7406</li>
        <li>\u827a\u672f \u2194 \u6587\u5b66</li>
        <li>\u5386\u53f2 \u2194 \u519b\u4e8b</li>
        <li>\u903b\u8f91 \u2194 \u6570\u5b66 \u2194 \u79d1\u5b66</li>
      </ol>
    </div>
''')

# 05 如何读 & 结语
parts.append('''    <h2 class="sec-head" id="method"><span class="no">05</span>\u5982\u4f55\u8bfb\u6bcf\u4e00\u8f91</h2>
    <p>\u4e09\u5341\u516d\u8f91\u5f62\u4f53\u7edf\u4e00\uff0c\u8bfb\u6cd5\u4e5f\u53ef\u4ee5\u7edf\u4e00\u3002</p>
    <div class="method-grid">
      <div class="method"><h4>\u601d\u7ef4\u5bfc\u56fe \u2014\u2014 \u5148\u770b\u56fe\uff0c\u518d\u770b\u5b57</h4><p>\u6bcf\u7ae0\u5f00\u5934\u4e00\u5f20\u601d\u7ef4\u5bfc\u56fe\uff0c\u662f\u6574\u4e2a\u6d3e\u7cfb/\u7ae0\u8282\u7684\u201c\u9aa8\u67b6\u201d\u3002</p></div>
      <div class="method"><h4>\u5bf9\u7167\u8868 \u2014\u2014 \u6293\u5bf9\u7acb\uff0c\u522b\u9009\u8fb9</h4><p>\u5bf9\u7167\u8868\u628a\u5bf9\u7acb\u7acb\u573a\u5e76\u6392\u6446\u51fa\u3002\u91cd\u70b9\u4e0d\u662f\u8bb0\u8c01\u5bf9\u8c01\u9519\u3002</p></div>
      <div class="method"><h4>\u4eba\u7269\u8bed\u5f55 \u2014\u2014 \u54c1\u539f\u610f\uff0c\u89c1\u5176\u4eba</h4><p>\u8bed\u5f55\u662f\u601d\u60f3\u5bb6\u7684\u201c\u539f\u58f0\u201d\u3002\u8bfb\u4e00\u53e5\u8bed\u5f55\uff0c\u8bd5\u7740\u8fd8\u539f\u5b83\u80cc\u540e\u7684\u65f6\u4ee3\u95ee\u9898\u3002</p></div>
      <div class="method"><h4>\u5386\u53f2\u80cc\u666f \u2014\u2014 \u653e\u5230\u65f6\u4ee3\u91cc</h4><p>\u6ca1\u6709\u4e00\u79cd\u601d\u60f3\u8131\u79bb\u65f6\u4ee3\u3002\u95ee\u4e00\u53e5\uff1a\u5b83\u662f\u5bf9\u5f53\u65f6\u4ec0\u4e48\u56f0\u5883\u7684\u56de\u7b54\uff1f</p></div>
    </div>
    <div class="intro-card">
      <h3>\u4e00\u4efd\u201c\u4e09\u95ee\u201d\u8bfb\u4e66\u5361</h3>
      <p>\u6bcf\u8bfb\u5b8c\u4e00\u7ae0\uff0c\u7528\u4e09\u4e2a\u95ee\u9898\u81ea\u6d4b\uff1a<strong>\u5b83\u5728\u56de\u7b54\u4ec0\u4e48\u95ee\u9898\uff1f</strong>\uff08\u52a8\u673a\uff09<strong>\u5b83\u7684\u6838\u5fc3\u4e3b\u5f20\u662f\u4ec0\u4e48\uff1f</strong>\uff08\u5185\u5bb9\uff09<strong>\u5b83\u4e0e\u8c01\u5bf9\u7acb\u3001\u727a\u7272\u4e86\u4ec0\u4e48\uff1f</strong>\uff08\u8fb9\u754c\uff09\u3002</p>
    </div>
    <div class="closing" id="closing">
      <p>\u601d\u60f3\u56fe\u8c31\u7cfb\u5217\u7684\u5168\u90e8\u7528\u610f\uff0c\u53ef\u4ee5\u7528\u4e00\u53e5\u8bdd\u6982\u62ec\uff1a<strong>\u5728\u4e00\u4e2a\u4fe1\u606f\u8fc7\u8f7d\u3001\u7acb\u573a\u6495\u88c2\u7684\u65f6\u4ee3\uff0c\u5e2e\u4f60\u91cd\u65b0\u83b7\u5f97\u201c\u60f3\u6e05\u695a\u201d\u548c\u201c\u5b89\u987f\u81ea\u5df1\u201d\u7684\u80fd\u529b\u3002</strong></p>
      <p>\u4f60\u53ef\u4ee5\u4ece\u4efb\u4f55\u4e00\u8f91\u5f00\u59cb\uff0c\u4f46\u82e5\u6709\u65f6\u95f4\uff0c\u8bf7\u6cbf\u7740\u516b\u9636\u7684\u987a\u5e8f\u8d70\u4e00\u904d\u3002\u8fd9\u6761\u5f27\u7ebf\uff0c\u6b63\u662f\u901a\u8bc6\u6559\u80b2\u6700\u53e4\u8001\u3001\u4e5f\u6700\u6839\u672c\u7684\u8bb8\u8bfa\uff1a<strong>\u8ba9\u4eba\u6210\u4e3a\u5b8c\u6574\u7684\u4eba\u3002</strong></p>
      <span class="sig">\u2014\u2014 \u601d\u60f3\u56fe\u8c31\u7cfb\u5217 \u00b7 \u9605\u8bfb\u6307\u5357 \u00b7 \u5171 ''' + str(len(VOLUMES)) + ''' \u8f91 \u00b7 \u8a79\u5bb6\u6768\u3001\u8fdf\u541b\u8fbe</span>
    </div>
    <footer>\u601d\u60f3\u56fe\u8c31\u7cfb\u5217 \u00b7 \u9605\u8bfb\u6307\u5357\u4e0e\u9636\u6bb5\u5212\u5206\u8bf4\u660e \u00b7 \u539f\u521b\u4f5c\u8005\uff1a\u8a79\u5bb6\u6768\u3001\u8fdf\u541b\u8fbe \u00b7 \u7531 Trae Work \u751f\u6210 \u00b7 \u6570\u636e\u66f4\u65b0\u4e8e 2026-09-06</footer>
  </article>
</div>
</body>
</html>''')

# 合并写入
html = "".join(parts)
out_path = os.path.join(BASE, "\u601d\u60f3\u56fe\u8c31\u7cfb\u5217", "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("\n\u2713 \u9605\u8bfb\u6307\u5357\u5df2\u751f\u6210: %s" % out_path)
print("  \u5927\u5c0f: %d \u5b57\u8282 (%s KB)" % (len(html), round(len(html)/1024, 1)))

# 验证
vol_count = html.count("VOL.")
print("  VOL. \u6807\u8bb0: %d \u4e2a" % vol_count)

# 同步桌面
shutil.copy2(out_path, os.path.join(r"C:\Users\Admin1\Desktop\Trae资料库", "index.html"))
print("\u2713 \u5df2\u540c\u6b65\u5230\u684c\u9762")