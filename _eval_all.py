import os
import re
import json

base = r"c:\Users\Admin1\Documents\FastViewCloudService"

# 卷目录 -> HTML 文件映射（排除 思想图谱系列 阅读指南区）
vol_dirs = [
    "isms-glossary", "truth-dimensions", "marxism-lineage", "liberalism-lineage",
    "eastern-thought-lineage", "series-overview", "economics-lineage", "science-lineage",
    "art-aesthetics-lineage", "ethics-lineage", "law-lineage", "tech-ai-lineage",
    "history-lineage", "military-lineage", "social-thought", "econ-part2-lineage",
    "philosophy-lineage", "psych-lineage", "education-lineage", "logic-lineage",
    "literature-lineage", "math-lineage", "politics-lineage", "ir-lineage",
    "life-science-lineage", "geo-lineage", "media-lineage", "rhetoric-lineage",
    "anthropology-lineage", "physics-lineage", "astronomy-lineage", "chemistry-lineage",
    "medicine-lineage", "religion-lineage", "linguistics-lineage", "cs-lineage",
]

html_names = {
    "isms-glossary": "政治基础概念1.html",
}
# 其余卷用 {dir}/{dir}.html

results = []
for d in vol_dirs:
    fn = html_names.get(d, f"{d}.html")
    hp = os.path.join(base, d, fn)
    if not os.path.exists(hp):
        results.append({"dir": d, "error": "FILE NOT FOUND"})
        continue
    size = os.path.getsize(hp)
    content = open(hp, encoding="utf-8", errors="replace").read()
    lines = content.count("\n") + 1

    # 正文中文字符数（去标签）
    text = re.sub(r"<[^>]+>", "", content)
    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", text))

    stats = {
        "dir": d,
        "size_kb": round(size / 1024, 1),
        "lines": lines,
        "zh_chars": zh_chars,
        "mermaid": len(re.findall(r'class="mermaid"', content)),
        "diagram": len(re.findall(r'class="diagram"', content)),
        "explain": len(re.findall(r'<div class="explain"', content)),
        "legacy_who": len(re.findall(r'class="legacy-who"', content)),
        "table": len(re.findall(r"<table", content)),
        "sec": len(re.findall(r'class="sec"', content)),
        "h2": len(re.findall(r"<h2[ >]", content)),
    }
    results.append(stats)

# 输出表格
print(f"{'卷目录':<28}{'KB':>6}{'行数':>7}{'汉字':>7}{'导图':>5}{'图表':>5}{'解释':>5}{'语录':>5}{'表格':>5}{'章节':>5}")
for r in sorted(results, key=lambda x: x.get("size_kb", 0), reverse=True):
    if "error" in r:
        print(f"{r['dir']:<28}  ERROR")
        continue
    print(f"{r['dir']:<28}{r['size_kb']:>6}{r['lines']:>7}{r['zh_chars']:>7}{r['mermaid']:>5}{r['diagram']:>5}{r['explain']:>5}{r['legacy_who']:>5}{r['table']:>5}{r['sec']:>5}")

json.dump(results, open(r"c:\Users\Admin1\Documents\FastViewCloudService\_eval_results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n已保存 _eval_results.json")
