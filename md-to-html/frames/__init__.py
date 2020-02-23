import xml.etree.ElementTree as etree
from re import sub

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor

"""
Github式<h>
"""
class AddHref(Postprocessor):
    def run(self, text):
        return sub(r'<h(\d) id=([\'"])(.*?)\2>(.*?)</h\1>', r"<h\1 id='\3'><a id='\3' href='#\3'>\4</a></h\1>", text)

class AddHrefExt(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(AddHref(), 'add_href', 175)

"""
<del>
"""
class DelTag(InlineProcessor):
    def handleMatch(self, m, data):
        p = etree.Element('del')
        p.text = m.group(1)
        return p, m.start(), m.end()

class DelTagExt(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(DelTag(r"\~\~(.*?)\~\~"), 'del_tag', 70)


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

all_ext = [AddHrefExt(), LargeFontExt(), DelTagExt()]
