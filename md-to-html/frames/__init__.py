from markdown.postprocessors import Postprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree
from re import sub, search, DOTALL

"""
Github式<h>
"""
class AddHref(Postprocessor):
    def run(self, text):
        self.count = 0
        return sub(r'<h(\d)>(.*?)</h\1>', self.do_, text)

    def do_(self, m):
        self.count += 1
        return "<h{0}><a id='{1}_{2}' href='#{1}_{2}'>{3}</a></h{0}>".format(m.group(1), sub('<.*?>', '', m.group(2)), self.count, m.group(2))

class AddHrefExt(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(AddHref(), 'add_href', 175)

"""
自定义字体大小
"""
class LargeFont(InlineProcessor):
    def handleMatch(self, m, data):
        p = etree.Element('span')
        p.set('style', f'font-size: {m.group(2)}rem')
        p.text = m.group(3)
        return p, m.start(), m.end()

class LargeFontExt(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(LargeFont(r"(\$([\d.]*)￥)(.*?)\1"), 'large_font', 175)

all_ext = [AddHrefExt(), LargeFontExt()]
