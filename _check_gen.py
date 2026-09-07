import os, re

BASE = r"C:\Users\Admin1\Documents\FastViewCloudService"
fp = os.path.join(BASE, "series-overview", "series-overview.html")

if os.path.exists(fp):
    size = os.path.getsize(fp)
    print(f"文件已生成: {size/1024:.0f} KB")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    lines = len(c.split("\n"))
    print(f"行数: {lines}")
    for kw in ["收束", "36", "三十六", "VOL.36", "mermaid", "星图", "知识树", "stage", "阶段"]:
        count = len(re.findall(kw, c))
        print(f"  '{kw}': {count} 处")
else:
    print("文件尚未生成")