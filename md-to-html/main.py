from json import load, dump
from re import sub

from PyQt5.Qt import *

from frames.head import Head
from frames.setting import Set
from frames.work import Work


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.conf, self.css = None, None
        self.menu = self.menuBar()
        font_id = QFontDatabase.addApplicationFont("files/iconfont.ttf")
        self.ico_font = QFont(QFontDatabase.applicationFontFamilies(font_id)[0], 30)
        self.has_opened_file = 'default'

        self.frame_head = Head(self)
        self.frame_work = Work(self)
        self.frame_set = Set(self)

        self.init()

        desktop = QApplication.desktop().screenGeometry()
        size = self.conf['size']
        self.setGeometry(int(desktop.width() / 2 - size[0] / 2), int(desktop.height() / 2 - size[1] / 2), size[0],
                         size[1])

    def init(self):
        with open("files/conf.json", encoding="UTF-8") as f:
            self.conf = load(f)
        self.set_stylesheet()
        with open("files/style.css", encoding="UTF-8") as f:
            self.css = f.read()
        self.frame_head.init()
        self.frame_work.init()
        self.frame_set.init()
        self.init_menu()

        middle = QWidget(self)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 3, 0, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 10)
        layout.addWidget(self.frame_head, 0, 0)
        layout.addWidget(self.frame_work, 1, 0)
        middle.setLayout(layout)
        self.setCentralWidget(middle)

    def init_menu(self):
        file_menu = self.menu.addMenu('文件')
        set_menu = self.menu.addMenu('设置')
        about_menu = self.menu.addMenu('关于')
        for menu in [file_menu, set_menu, about_menu]:
            menu.setCursor(Qt.PointingHandCursor)
        open_action = QAction('打开', self)
        open_action.triggered.connect(self.open_md)
        new_action = QAction('新建', self)
        new_action.triggered.connect(self.new_md)
        save_action = QAction('保存', self)
        save_action.triggered.connect(self.save_md)
        file_menu.addActions([open_action, new_action, save_action])

        choose_color = QMenu('主题', self)
        white_theme = QAction('白色', self)
        white_theme.setProperty("color", "white")
        dark_theme = QAction('黑色', self)
        dark_theme.setProperty("color", "dark")
        wheat_theme = QAction('小麦', self)
        wheat_theme.setProperty("color", "wheat")
        for t in [white_theme, dark_theme, wheat_theme]:
            t.triggered.connect(self.choose_theme)
            choose_color.addAction(t)
        set_menu.addMenu(choose_color)
        font_big = QAction("字体增", self)
        font_sma = QAction("字体减", self)
        for f in [font_big, font_sma]:
            f.triggered.connect(self.change_font)
            set_menu.addAction(f)

    def save_conf(self):
        with open('files/conf.json', 'w', encoding='utf-8') as f:
            dump(self.conf, f, indent=4)

    """ 文件 """
    def open_md(self):
        if self.ask_save():
            return
        self.frame_work.ipt.setPlainText('')
        path = QFileDialog.getOpenFileName(self, '选择文件', '', '*.md')
        if path[0]:
            with open(path[0], 'r', encoding='utf-8') as f:
                self.frame_work.ipt.setPlainText(f.read())
                self.has_opened_file = path[0]

    def new_md(self):
        if self.ask_save():
            return
        self.frame_work.ipt.setPlainText('新建成功,请输入md文档吧')
        self.has_opened_file = 'new_file'

    def save_md(self):
        if self.has_opened_file in ['new_file', 'default']:
            f = QFileDialog.getSaveFileName(self, '新建MD文件', '', '*.md')
            if f[0]:
                path = f[0]
            else:
                return False
        elif self.has_opened_file:
            path = self.has_opened_file
        else:
            return False
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.frame_work.ipt.toPlainText())
            QMessageBox.information(self, '成功', '保存完成!', QMessageBox.Ok)
            self.has_opened_file = False
            return True

    def ask_save(self):
        if self.has_opened_file != 'default' or self.frame_work.ipt.toPlainText():
            r = QMessageBox.warning(self, "提醒", "是否保存当前文件?", QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if r == QMessageBox.Ok:
                if not self.save_md():
                    return True
            elif r == QMessageBox.Cancel:
                return True

    """ 设置 """
    def set_stylesheet(self):
        with open("files/style.qss", encoding="UTF-8") as f:
            s = sub(r'([\d.]*)rem', lambda m: str(int(float(m.group(1))*self.conf['font-size']))+'px', f.read())
            s = sub('theme', self.conf['theme'][self.conf['choose_theme']], s)
            self.setStyleSheet(s)

    def choose_theme(self):
        self.conf["choose_theme"] = self.sender().property("color")
        self.set_stylesheet()
        self.save_conf()

    def change_font(self):
        if self.sender().text() == '字体增':
            self.conf['font-size'] += 1
        else:
            self.conf['font-size'] -= 1
        self.set_stylesheet()
        self.save_conf()

if __name__ == '__main__':
    from sys import argv

    app = QApplication(argv)
    main = Main()
    main.show()
    app.exec_()