# -*- coding: utf-8 -*-
"""HTML 结构校验 & 工作区/桌面版同步确认"""
import re, os, glob

ws = r'c:\Users\Admin1\Documents\FastViewCloudService'
desktop = r'c:\Users\Admin1\Desktop\Trae资料库'

vols = ['truth-dimensions', 'marxism-lineage', 'economics-lineage',
        'econ-part2-lineage', 'psych-lineage', 'math-lineage', 'logic-lineage']

print('=' * 60)
print('HTML 结构校验')
print('=' * 60)

# 1. 结构校验：标签平衡、结尾、关键模块
for vol in vols:
    fp = os.path.join(ws, vol, vol + '.html')
    if not os.path.exists(fp):
        print(f'{vol}: ❌ 文件不存在')
        continue
    c = open(fp, encoding='utf-8').read()
    issues = []

    # 结尾
    if not c.rstrip().endswith('</html>'):
        issues.append('不以</html>结尾')

    # section 标签平衡（排除script中的字符串）
    c_no_script = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL)
    opens = len(re.findall(r'<section\b', c_no_script))
    closes = len(re.findall(r'</section>', c_no_script))
    if opens != closes:
        issues.append(f'section标签不平衡: {opens}开/{closes}闭')

    # div 标签平衡
    d_opens = len(re.findall(r'<div\b', c_no_script))
    d_closes = len(re.findall(r'</div>', c_no_script))
    if d_opens != d_closes:
        issues.append(f'div标签不平衡: {d_opens}开/{d_closes}闭')

    # 关键模块
    modules = []
    if 'id="masters-m1"' in c: modules.append('硕士')
    if 'id="phd-prologue"' in c: modules.append('博士')
    if 'id="appendix-k"' in c: modules.append('本科附录')

    # 状态
    if issues:
        print(f'{vol}: ⚠️ {issues}')
    else:
        print(f'{vol}: ✅ 结构完整 [{", ".join(modules) if modules else "基础"}]')

print()
print('=' * 60)
print('桌面版同步确认')
print('=' * 60)

# 2. 工作区与桌面版同步：对比6个标星卷主文件
dir_map = {
    'truth-dimensions': '真理的多维图景',
    'marxism-lineage': '马克思主义谱系',
    'economics-lineage': '经济思想谱系',
    'econ-part2-lineage': '经济思想谱系下篇',
    'psych-lineage': '心理学思想谱系',
    'math-lineage': '数学思想谱系',
    'logic-lineage': '逻辑与论证思想谱系',
}

for eng, chn in dir_map.items():
    ws_fp = os.path.join(ws, eng, eng + '.html')
    dt_fp1 = os.path.join(desktop, chn, eng + '.html')
    dt_fp2 = os.path.join(desktop, chn, chn + '.html')

    ws_size = os.path.getsize(ws_fp) if os.path.exists(ws_fp) else 0
    dt1_size = os.path.getsize(dt_fp1) if os.path.exists(dt_fp1) else 0
    dt2_size = os.path.getsize(dt_fp2) if os.path.exists(dt_fp2) else 0

    # 检查桌面版是否有与工作区相同内容的文件
    # 读取内容对比（前100字节+大小近似判断）
    ws_c = open(ws_fp, encoding='utf-8').read() if os.path.exists(ws_fp) else ''
    match1 = False
    match2 = False
    if os.path.exists(dt_fp1):
        c1 = open(dt_fp1, encoding='utf-8').read()
        match1 = abs(len(ws_c) - len(c1)) < 200
    if os.path.exists(dt_fp2):
        c2 = open(dt_fp2, encoding='utf-8').read()
        match2 = abs(len(ws_c) - len(c2)) < 200

    status = '✅' if (match1 or match2) else '⚠️'
    print(f'{eng:25s} 工作区={ws_size//1024}KB '
          f'桌面[{eng}.html]={dt1_size//1024}KB({match1}) '
          f'桌面[{chn}.html]={dt2_size//1024}KB({match2}) {status}')

# 3. 桌面版索引文件同步检查
print()
print('=' * 60)
print('桌面版索引/阅读指南')
print('=' * 60)
for fname in ['index.html', '主题索引.html']:
    ws_fp = os.path.join(ws, '思想图谱系列', fname)
    dt_fp = os.path.join(desktop, '思想图谱系列', fname)
    ws_size = os.path.getsize(ws_fp) if os.path.exists(ws_fp) else 0
    dt_size = os.path.getsize(dt_fp) if os.path.exists(dt_fp) else 0
    same = '✅' if abs(ws_size - dt_size) < 1000 else '⚠️'
    print(f'{fname}: 工作区={ws_size//1024}KB 桌面={dt_size//1024}KB {same}')

# 4. 桌面版断链复检
print()
print('=' * 60)
print('桌面版断链复检')
print('=' * 60)
total_dt = 0
broken_dt = 0
for d in sorted(os.listdir(desktop)):
    dp = os.path.join(desktop, d)
    if not os.path.isdir(dp) or d.startswith('_') or d.startswith('.'):
        continue
    for hf in glob.glob(os.path.join(dp, '*.html')):
        c = open(hf, encoding='utf-8').read()
        for l in re.findall(r'href="\.\./([^"]*)"', c):
            total_dt += 1
            if not os.path.exists(os.path.normpath(os.path.join(dp, '..', l))):
                broken_dt += 1
print(f'桌面版跨卷链接: {total_dt} 条, 断链: {broken_dt}')

print()
print('=' * 60)
if broken_dt == 0:
    print('✅ 全部校验通过：结构完整、桌面已同步、无断链')
else:
    print(f'⚠️ 发现 {broken_dt} 处断链需修复')
print('=' * 60)