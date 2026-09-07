# -*- coding: utf-8 -*-
"""思想图谱系列 · 新辑生成脚本：生成 8 辑 HTML 并复制共享资源（工作区 + 桌面版）"""

import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import _gen_data_a as a
import _gen_data_b as b
from _gen_lib import build_html

VOLUMES = [a.MATH, a.POLITICS, a.IR, a.BIO, b.GEO, b.MEDIA, b.RHETORIC, b.ANTHROPOLOGY]

# 桌面版中文文件夹名
DT_FOLDER = {
    "math-lineage": "数学思想谱系",
    "politics-lineage": "政治学通论",
    "ir-lineage": "国际关系思想谱系",
    "bio-lineage": "生命科学思想谱系",
    "geo-lineage": "地理与环境思想谱系",
    "media-lineage": "传播与媒介思想谱系",
    "rhetoric-lineage": "修辞与演说思想谱系",
    "anthropology-lineage": "人类学思想谱系",
}

DESKTOP_ROOT = r"C:\Users\Admin1\Desktop\Trae资料库"
STAGING_ROOT = os.path.join(BASE, "_desktop_staging")  # 沙箱内暂存目录，生成后由 PowerShell 复制到桌面

SRC_DIR = os.path.join(BASE, "literature-lineage")  # 工作区共享资源来源
DT_SRC_DIR = os.path.join(DESKTOP_ROOT, "逻辑与论证思想谱系")  # 桌面版共享资源来源


def ensure_shared(dst_dir, src_dir):
    """复制 assets/main.js 与 _shared 资源到目标辑目文件夹"""
    for rel in ["assets/main.js", "_shared/js/mermaid.min.js"]:
        src = os.path.join(src_dir, rel)
        dst = os.path.join(dst_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    fonts_src = os.path.join(src_dir, "_shared", "fonts")
    fonts_dst = os.path.join(dst_dir, "_shared", "fonts")
    os.makedirs(fonts_dst, exist_ok=True)
    for f in os.listdir(fonts_src):
        if not os.path.exists(os.path.join(fonts_dst, f)):
            shutil.copy2(os.path.join(fonts_src, f), os.path.join(fonts_dst, f))


def gen_workspace():
    for v in VOLUMES:
        folder = os.path.join(BASE, v["ws_folder"])
        os.makedirs(folder, exist_ok=True)
        html = build_html(v, desktop=False)
        out = os.path.join(folder, v["ws_file"])
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        ensure_shared(folder, SRC_DIR)
        print("工作区已生成：%s · %s" % (v["no_label"], v["title"]))


def gen_desktop():
    for v in VOLUMES:
        dt_name = DT_FOLDER[v["ws_folder"]]
        folder = os.path.join(STAGING_ROOT, dt_name)
        os.makedirs(folder, exist_ok=True)
        html = build_html(v, desktop=True)
        out = os.path.join(folder, dt_name + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        ensure_shared(folder, DT_SRC_DIR)
        print("桌面版已暂存：%s · %s" % (v["no_label"], v["title"]))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--desktop", action="store_true", help="仅生成桌面版")
    p.add_argument("--workspace", action="store_true", help="仅生成工作区版")
    args = p.parse_args()
    if args.desktop:
        gen_desktop()
    elif args.workspace:
        gen_workspace()
    else:
        gen_workspace()
        gen_desktop()
