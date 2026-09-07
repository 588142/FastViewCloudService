# -*- coding: utf-8 -*-
"""将工作区目录页转换为桌面版（中文文件夹路径）"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "思想图谱系列", "index.html")
OUT = os.path.join(BASE, "_desktop_staging", "index.html")

# 工作区英文文件夹 -> 桌面版中文文件夹
FOLDER_MAP = {
    "logic-lineage": "逻辑与论证思想谱系",
    "philosophy-lineage": "西方哲学思想谱系",
    "eastern-thought": "东方思想谱系",
    "truth-dimensions": "真理的多维图景",
    "math-lineage": "数学思想谱系",
    "social-thought": "社会思想谱系",
    "politics-lineage": "政治学通论",
    "ir-lineage": "国际关系思想谱系",
    "anthropology-lineage": "人类学思想谱系",
    "marxism-lineage": "马克思主义谱系",
    "liberalism-lineage": "自由主义谱系",
    "law-lineage": "法哲学思想谱系",
    "ethics-lineage": "伦理与道德思想谱系",
    "economics-lineage": "经济思想谱系",
    "econ-thought": "经济思想谱系下篇",
    "science-lineage": "科学思想谱系",
    "bio-lineage": "生命科学思想谱系",
    "geo-lineage": "地理与环境思想谱系",
    "history-lineage": "历史思想谱系",
    "military-lineage": "军事与战略思想谱系",
    "tech-ai-lineage": "科技与人工智能思想谱系",
    "art-aesthetics": "艺术与美学思想谱系",
    "psych-lineage": "心理学思想谱系",
    "literature-lineage": "文学与语言思想谱系",
    "media-lineage": "传播与媒介思想谱系",
    "rhetoric-lineage": "修辞与演说思想谱系",
    "edu-lineage": "教育思想谱系",
    "series-overview": "系列总览",
}

# 文件名映射（工作区文件名 -> 桌面版文件名）
FILE_MAP = {
    "logic-lineage.html": "逻辑与论证思想谱系.html",
    "philosophy-lineage.html": "西方哲学思想谱系.html",
    "eastern-thought.html": "东方思想谱系.html",
    "政治基础概念1.html": "政治基础概念1.html",
    "truth-dimensions.html": "真理的多维图景.html",
    "math-lineage.html": "数学思想谱系.html",
    "social-thought.html": "社会思想谱系.html",
    "politics-lineage.html": "政治学通论.html",
    "ir-lineage.html": "国际关系思想谱系.html",
    "anthropology-lineage.html": "人类学思想谱系.html",
    "marxism-lineage.html": "马克思主义谱系.html",
    "liberalism-lineage.html": "自由主义谱系.html",
    "law-lineage.html": "法哲学思想谱系.html",
    "ethics-lineage.html": "伦理与道德思想谱系.html",
    "economics-lineage.html": "经济思想谱系.html",
    "econ-thought.html": "经济思想谱系下篇.html",
    "science-lineage.html": "科学思想谱系.html",
    "bio-lineage.html": "生命科学思想谱系.html",
    "geo-lineage.html": "地理与环境思想谱系.html",
    "history-lineage.html": "历史思想谱系.html",
    "military-lineage.html": "军事与战略思想谱系.html",
    "tech-ai-lineage.html": "科技与人工智能思想谱系.html",
    "art-aesthetics.html": "艺术与美学思想谱系.html",
    "psych-lineage.html": "心理学思想谱系.html",
    "literature-lineage.html": "文学与语言思想谱系.html",
    "media-lineage.html": "传播与媒介思想谱系.html",
    "rhetoric-lineage.html": "修辞与演说思想谱系.html",
    "edu-lineage.html": "教育思想谱系.html",
    "series-overview.html": "系列总览.html",
}

with open(SRC, encoding="utf-8") as f:
    html = f.read()

# 1. 字体路径
html = html.replace("../isms-glossary/_shared/fonts/", "./政治基础概念1/_shared/fonts/")

# 2. 卷链接：../<ws_folder>/<ws_file> -> ./<中文名>/<中文名>.html
for ws_folder, dt_folder in FOLDER_MAP.items():
    for ws_file, dt_file in FILE_MAP.items():
        if ws_file.startswith(ws_folder + ".") or ws_file == "政治基础概念1.html":
            pass
    # 通用替换：../<ws_folder>/<任意>.html
    import re
    html = re.sub(
        r'\.\./%s/([^"\'#]+\.html)' % re.escape(ws_folder),
        lambda m: "./%s/%s" % (dt_folder, FILE_MAP.get(m.group(1), m.group(1))),
        html,
    )

# 3. 特殊：政治基础概念1（工作区在 isms-glossary 下）
html = re.sub(
    r'\.\./isms-glossary/([^"\'#]+\.html)',
    lambda m: "./政治基础概念1/%s" % FILE_MAP.get(m.group(1), m.group(1)),
    html,
)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("桌面版目录页已暂存：", OUT)
