# -*- coding: utf-8 -*-
"""思想图谱系列 · 构建工具
用法:
  python build.py export <html相对路径> [--dest DIR]   导出单卷为可独立分发的自包含副本
  python build.py verify [--root DIR]                   引用完整性 + DOM 审计
  python build.py sync                                  同步桌面版/OneDrive 双镜像
"""
import os, re, sys, shutil, subprocess, argparse

ROOT = r'c:\Users\Admin1\Documents\FastViewCloudService'

def collect_refs(c):
    """收集 html 中所有相对 _shared 引用"""
    out = []
    out += re.findall(r'(?:src|href)="((?:\.{1,2}/)[^"]*_shared/[^"]+)"', c)
    out += re.findall(r"url\(['\"]?((?:\.{1,2}/)[^'\"()]*_shared/[^'\"()]+)['\"]?\)", c)
    return set(out)

def cmd_export(html_rel, dest):
    src = os.path.join(ROOT, html_rel)
    if not os.path.exists(src):
        print(f'找不到文件: {src}'); return 1
    dest = dest or os.path.join(ROOT, '_export', os.path.splitext(os.path.basename(html_rel))[0])
    os.makedirs(dest, exist_ok=True)
    c = open(src, encoding='utf-8').read()
    base = os.path.dirname(src)
    copied = set()
    for r in collect_refs(c):
        t = os.path.normpath(os.path.join(base, r))
        if not os.path.exists(t):
            print(f'  ! 源缺失: {r}'); continue
        rel = r.lstrip('./')
        dst = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if dst not in copied and not os.path.exists(dst):
            shutil.copy2(t, dst)
        copied.add(dst)
        c = c.replace(r, r.replace('../_shared/', './_shared/'))
    out_html = os.path.join(dest, os.path.basename(html_rel))
    with open(out_html, 'w', encoding='utf-8') as fh:
        fh.write(c)
    print(f'导出完成: {dest} ({os.path.basename(html_rel)})')
    return 0

def cmd_verify(root):
    subprocess.run([sys.executable, os.path.join(ROOT, '_verify_dedupe.py')])
    return subprocess.run([sys.executable, os.path.join(ROOT, '_audit_dom.py'), root]).returncode

def cmd_sync():
    src = os.path.join(ROOT, '思想图谱系列')
    for tgt in [r'C:\Users\Admin1\Desktop\Trae资料库',
                r'C:\Users\Admin1\OneDrive\思想图谱系列\Trae资料库']:
        r = subprocess.run(['robocopy', src, tgt, '/MIR', '/NFL', '/NDL', '/NJH', '/NP'],
                           capture_output=True, text=True)
        print(f'{tgt}: exit={r.returncode}')
    return 0

def main():
    ap = argparse.ArgumentParser(description='思想图谱系列构建工具')
    sub = ap.add_subparsers(dest='cmd')
    p_exp = sub.add_parser('export')
    p_exp.add_argument('html_rel')
    p_exp.add_argument('--dest')
    p_verify = sub.add_parser('verify')
    p_verify.add_argument('--root', default=ROOT)
    sub.add_parser('sync')
    args = ap.parse_args()
    if args.cmd == 'export':
        return cmd_export(args.html_rel, args.dest)
    if args.cmd == 'verify':
        return cmd_verify(args.root)
    if args.cmd == 'sync':
        return cmd_sync()
    ap.print_help()
    return 0

if __name__ == '__main__':
    sys.exit(main())
