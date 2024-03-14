from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QTextEdit

from ReadIni import AllQss, DayQss, NightQss
from ToolFun import GetTheme
from ZEBqt import EnbuBasicWindow


# 自动改变大小的文本编辑框
class AutoResizeTextEdit(QTextEdit):
    def __init__(self, name, dad):
        super(AutoResizeTextEdit, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.AutoResize()

    def AutoResize(self):
        temp_qss = DayQss if self.Theme == "Day" else NightQss
        self.mybar = QtWidgets.QScrollBar()  # 我的滚动条
        # 给这个滚动条添加属性
        self.mybar.setStyleSheet("""
             QScrollBar:vertical {
                  border-radius: 2px;
                  border: none;
                  background:rgba(0, 0, 0, 0);
                  width:10px;

              }
              QScrollBar::handle:vertical {
                  background:  %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 0px;
              }
              QScrollBar::handle:vertical:hover {
                  background: %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 1px 0px 1px;
              }
              QScrollBar::add-line:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0 rgba(0, 0, 0, 0), stop: 0.5 rgba(0, 0, 0, 0),  stop:1 rgba(0, 0, 0, 0));
                  height: 0px;
              }
              QScrollBar::sub-line:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0  rgba(0, 0, 0, 0), stop: 0.5 rgba(0, 0, 0, 0),  stop:1 rgba(0, 0, 0, 0));
                  height: 0 px;
              }
              QScrollBar::sub-page:vertical {
              background: rgba(0, 0, 0, 0);
              }

              QScrollBar::add-page:vertical {
              background: rgba(0, 0, 0, 0);
              }
              """ % (temp_qss.stroke_color1, temp_qss.theme_color))
        self.setVerticalScrollBar(self.mybar)  # 把滚动条附上去

    def myresize(self):
        vertical_scrollbar = self.verticalScrollBar()

        # 让文本居中对齐
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        block = self.document().findBlockByLineNumber(0)
        while block.isValid():
            cursor.setPosition(block.position())
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            cursor.setCharFormat(self.currentCharFormat())
            blockFormat = QTextBlockFormat()
            blockFormat.setAlignment(Qt.AlignCenter)
            cursor.setBlockFormat(blockFormat)
            block = block.next()

        # 调整窗口大小
        while vertical_scrollbar.isVisible():
            self.setMinimumHeight(self.height() + 1)
            self.dad.resize(self.dad.width(), self.dad.height() + 1)
            self.dad.BackGround.resize(self.dad.BackGround.width(), self.dad.BackGround.height() + 1)

            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

# 主窗口类
class AlertWindow(EnbuBasicWindow):
    def __init__(self, dad, mod, text):
        super(AlertWindow, self).__init__()
        self.Theme = dad.Theme  # 储存深浅色
        self.color = ""
        self.dad = dad
        self.mod = mod
        self.text = text
        self.resize(400, 250)  # 尺寸
        self.SetUp()

    def UIinit(self):
        self.BackGround  = QLabel('', self)         # 背景
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.Marking     = QLabel('', self)         # 标记文本（!/?）
        self.AlertText   = AutoResizeTextEdit('', self)         # 警告文本

        self.layout = QVBoxLayout()  # 一个纵向布局

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if GetTheme(self.Theme) == "Day" else NightQss
        if self.mod == "🤯":
            self.color = "#ff4659"
        else:
            self.color = temp_qss.theme_color

        # 背景
        self.BackGround.setStyleSheet('''background-color: %s ;
                                        border: 1px solid %s;
                                        border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))
        self.BackGround.setGraphicsEffect(self.Get_Shaow())

        # 标记文本
        self.Marking.setMinimumSize(60, 60)
        self.Marking.setMaximumSize(60, 60)
        self.Marking.setStyleSheet('''background-color: %s ;
                                        border: 0px;
                                        color:#ffffff;
                                        border-radius: 30px;''' % (self.color))
        # 显示的标题
        self.Marking.setFont(QtGui.QFont("arial", AllQss.font_size + 22))
        self.Marking.setText(QtCore.QCoreApplication.translate("MainWindow", self.mod))
        self.Marking.setAlignment(Qt.AlignCenter)

        # 显示的内容
        self.AlertText.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.AlertText.setText(QtCore.QCoreApplication.translate("MainWindow", self.text))
        self.AlertText.setAlignment(Qt.AlignCenter)
        self.AlertText.setStyleSheet('''border: 0px;
                                        color:%s;''' % (temp_qss.font_color1))
        self.AlertText.setReadOnly(True)  # 设置QTextEdit为只读

        # 关闭
        self.CloseButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 20))
        self.CloseButton.setText(QtCore.QCoreApplication.translate("MainWindow", "知道了"))
        self.CloseButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 10px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 10px;border: 3px solid %s;color: %s;font-weight: bold;}''' %
            (self.color, "#ffffff", self.color, "#ffffff", "#ffffff"))
        self.CloseButton.setMinimumHeight(40)

    def UIsite(self):
        # 背景
        k = 25  # 边距变量
        self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))

        # 布局
        self.layout.addWidget(self.Marking, 1, Qt.AlignHCenter)
        self.layout.addWidget(self.AlertText)
        self.layout.addWidget(self.CloseButton)
        self.BackGround.setLayout(self.layout)

    def UIfun(self):
        # 关闭按钮
        def ClossAll():
            self.close()
        self.CloseButton.clicked.connect(ClossAll)

    def show(self):
        super(AlertWindow, self).show()
        self.AlertText.myresize()


    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AlertWindow("", "✅", "请不要这样, sniaojdo iajdoia dija odijadjaoidja  adh oaid oai d adoaid oiaj daio doiajd oiaj doia wdaoisdjoaisjdoaijd ao")  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程