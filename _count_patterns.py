# -*- coding: utf-8 -*-
import re
c = open(r'c:\Users\Admin1\Documents\FastViewCloudService\marxism-lineage\marxism-lineage.html', encoding='utf-8').read()

p1 = '<div class="table-wrap">        <div class="table-wrap">'
p2 = '<div class="callout">        <div class="callout">'
p3 = ('</div>\n        <div class="callout">\n'
      '          <span class="callout-title">一条主线</span>        <div class="callout">\n'
      '          <span class="callout-title">一条主线</span>')
print(f'p1 (双table-wrap紧挨): {c.count(p1)}')
print(f'p2 (双callout紧挨): {c.count(p2)}')
print(f'p3 (一条主线块): {c.count(p3)}')

print('\ntable-wrap 双嵌套变体:')
for m in re.finditer(r'<div class="table-wrap">\s*<div class="table-wrap">', c):
    extra = len(m.group(0)) - len('<div class="table-wrap"><div class="table-wrap">')
    line = c[:m.start()].count('\n') + 1
    print(f'  @line {line}: 中间多余字符={extra}')

print('callout 双嵌套变体:')
for m in re.finditer(r'<div class="callout">\s*<div class="callout">', c):
    extra = len(m.group(0)) - len('<div class="callout"><div class="callout">')
    line = c[:m.start()].count('\n') + 1
    print(f'  @line {line}: 中间多余字符={extra}')
