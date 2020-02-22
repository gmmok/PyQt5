from re import sub

from PyQt5.Qt import *
from markdown import markdown

from frames import all_ext


class MdEdit(QTextEdit):
    def __init__(self, work):
        super(MdEdit, self).__init__(work)
        self.work = work
        self.top = work.top
        self.ext_list = ['attr_list', 'tables', 'fenced_code']
        self.ext_list.extend(all_ext)
        self.textChanged.connect(self.do_parse)

    def do_parse(self):
        content = self.toPlainText()
        content = markdown(content, extensions=self.ext_list)
        old_value = self.work.html.verticalScrollBar().value()
        self.work.html.setPlainText(content)
        self.work.html.verticalScrollBar().setValue(old_value)

class HtmlEdit(QTextEdit):
    def __init__(self, work):
        super(HtmlEdit, self).__init__(work)
        self.work = work
        self.top = work.top
        self.textChanged.connect(self.do_parse)

    def do_parse(self):
        old_value = self.verticalScrollBar().value()
        self.work.md.setText("<style>%s</style>" % self.top.css + sub(r'([\d.]*)rem', lambda m: str(int(float(m.group(1))*self.top.conf['font-size']))+'px', self.toPlainText()))
        self.verticalScrollBar().setValue(old_value)

class MdShow(QTextEdit):
    def __init__(self, work):
        super().__init__(work)
        self.work = work
        self.top = work.top
        self.setReadOnly(True)
        self.setStyleSheet("QTextEdit{background: transparent}")
