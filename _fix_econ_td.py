# -*- coding: utf-8 -*-
import re

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\_appendix_economics-lineage.html'
c = open(fp, encoding='utf-8').read()

# Locate the unbalanced td
td_o = len(re.findall(r'<td(?=[\s>])', c))
td_c = len(re.findall(r'</td>', c))
print(f'修复前: td 开={td_o} 闭={td_c} 差={td_o - td_c}')

# Find all <td> and </td> positions and their context
# Strategy: find all td tags and check if there's a missing closing tag
# Let's look at the last few td occurrences
all_td_open = [m.start() for m in re.finditer(r'<td(?=[\s>])', c)]
all_td_close = [m.start() for m in re.finditer(r'</td>', c)]

print(f'td_open count: {len(all_td_open)}, td_close count: {len(all_td_close)}')

# The issue is likely in a table where a <td> is missing its </td>
# Let's find the mismatched area by looking at the last td_open that doesn't have a corresponding close
# Check if the last <td> before the end of the file is closed
last_open_pos = all_td_open[-1]
last_close_pos = all_td_close[-1] if all_td_close else -1

# Get context around the last td_open
context_start = max(0, last_open_pos - 200)
context_end = min(len(c), last_open_pos + 500)
context = c[context_start:context_end]
print(f'\n最后一个 <td> 附近上下文:')
print(context[:600])
print('...')

# Check if there's a </td> after the last <td>
remaining_after_last = c[last_open_pos:]
remaining_close = len(re.findall(r'</td>', remaining_after_last))
print(f'\n最后一个 <td> 之后还有 {remaining_close} 个 </td>')

# Check if a <td> is inside a <tr> but missing </td> before </tr>
# Let's find <tr> blocks that have unbalanced td
tr_opens = [m.start() for m in re.finditer(r'<tr(?=[\s>])', c)]
tr_closes = [m.start() for m in re.finditer(r'</tr>', c)]

for i, tr_start in enumerate(tr_opens):
    tr_end = tr_closes[i] if i < len(tr_closes) else len(c)
    tr_content = c[tr_start:tr_end]
    tr_td_o = len(re.findall(r'<td(?=[\s>])', tr_content))
    tr_td_c = len(re.findall(r'</td>', tr_content))
    if tr_td_o != tr_td_c:
        print(f'\n<tr> #{i} 不平衡: td开={tr_td_o} 闭={tr_td_c} 差={tr_td_o - tr_td_c}')
        print(f'  <tr> 内容 (前200字符): {tr_content[:200]}')
        print(f'  <tr> 内容 (后200字符): {tr_content[-200:]}')