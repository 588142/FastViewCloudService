# -*- coding: utf-8 -*-
"""dump解析器栈在最后的关闭前"""
from html.parser import HTMLParser

fp = r'c:\Users\Admin1\Documents\FastViewCloudService\liberalism-lineage\liberalism-lineage.html'
c = open(fp, encoding='utf-8').read()

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.dump_done = False
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.stack.append((self.getpos(), dict(attrs).get('class', '')))
    def handle_endtag(self, tag):
        if tag == 'div':
            # 当处理到接近文件末尾的关闭时dump
            line = self.getpos()[0]
            if line >= 810 and not self.dump_done:
                self.dump_done = True
                print('行{} 关闭前栈 ({}层):'.format(line, len(self.stack)))
                for pos, cls in self.stack:
                    print('   {} @行{}'.format(cls[:40] or '(无class)', pos[0]))
            if self.stack:
                popped = self.stack.pop()
                if line >= 810:
                    print('   弹出: {} @行{}'.format((popped[1] or '(无class)')[:40], popped[0][0]))

p = P()
p.feed(c)
print()
print('最终未闭合:', [(pos, cls) for pos, cls in p.stack])
