import re

path = r"c:\Users\Admin1\Documents\FastViewCloudService\economics-lineage\economics-lineage.html"
content = open(path, encoding="utf-8").read()

# 精确看 class 写法
classes = re.findall(r'class="([^"]+)"', content)
from collections import Counter
cnt = Counter(classes)
print("== 出现 >=3 次的 class ==")
for c, n in cnt.most_common(40):
    if n >= 3:
        print(f"  {c}: {n}")

# 看 div class 结构样例（前几个常见 class 的上下文）
print("\n== 常见结构样例 ==")
for cls in ["explain", "cmp", "quote", "sec", "chapter"]:
    m = re.search(r'<div class="([^"]*' + cls + r'[^"]*)"[^>]*>', content)
    if m:
        print(f"  <div class=\"{m.group(1)}\"> ...")
