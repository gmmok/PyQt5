from PyQt5.Qt import *

from frames.Editor import MdEdit, HtmlEdit, MdShow


class Work(QFrame):
    def __init__(self, top):
        super(Work, self).__init__(top)
        self.top = top
        self.setObjectName("work")

        self.ipt = MdEdit(self)
        self.html = HtmlEdit(self)
        self.md = MdShow(self)

    def init(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.ipt)
        layout.addWidget(self.html)
        layout.addWidget(self.md)
        self.setLayout(layout)
        self.md.setVisible(False)
