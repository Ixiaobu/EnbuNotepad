from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QTextEdit

from ReadIni import AllQss, DayQss, NightQss
from ZEBqt import EnbuBasicWindow


# 自动改变大小的文本编辑框
class AutoResizeTextEdit(QTextEdit):
    def __init__(self, name, dad):
        super(AutoResizeTextEdit, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.setAcceptRichText(True)
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
class QuestionWindow(EnbuBasicWindow):
    def __init__(self, dad, mod, text, fun_false, fun_true):
        super(QuestionWindow, self).__init__()
        self.Theme = dad.Theme  # 储存深浅色
        self.mod = mod
        self.dad = dad
        self.text = text
        self.fun_false = fun_false
        self.fun_true = fun_true
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 设置窗口浮在最上方
        self.resize(400, 260)  # 尺寸
        self.SetUp()

    def UIinit(self):
        self.BackGround  = QLabel('', self)         # 背景
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.Marking     = QLabel('', self)         # 标记文本
        self.Text  = AutoResizeTextEdit('', self)  # 显示的文字
        self.YesButton = QPushButton('', self)  # 确定
        self.NoButton = QPushButton('', self)   # 拒绝

        self.layout = QVBoxLayout()  # 一个纵向布局

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

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
                                        border-radius: 30px;''' % (temp_qss.theme_color))
        # 显示的标题
        self.Marking.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 22))
        self.Marking.setText(QtCore.QCoreApplication.translate("MainWindow", self.mod))
        self.Marking.setAlignment(Qt.AlignCenter)  # 对齐

        self.Text.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Text.setText(self.text)
        self.Text.setAlignment(Qt.AlignCenter)
        self.Text.setStyleSheet('''border: 0px;
                                        color:%s;;''' % (temp_qss.font_color1))
        self.Text.setReadOnly(True)  # 设置QTextEdit为只读

        # 取小按钮
        self.NoButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.NoButton.setText(QtCore.QCoreApplication.translate("MainWindow", "取消"))
        self.NoButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.NoButton.setMinimumHeight(30)

        # 确定按钮
        self.YesButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.YesButton.setText(QtCore.QCoreApplication.translate("MainWindow", "确定"))
        self.YesButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.YesButton.setMinimumHeight(30)

        # 关闭
        self.CloseButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.CloseButton.setText(QtCore.QCoreApplication.translate("MainWindow", "×"))
        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

    def UIsite(self):
        # 背景
        k = 25  # 边距变量
        self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))

        # 关闭
        self.CloseButton.setGeometry(QtCore.QRect(self.width() - 45 - k, k - 5, 30, 30))

        # 布局
        self.layout.addWidget(self.Marking, 1, Qt.AlignHCenter)
        self.layout.addWidget(self.Text)
        self.layout.addWidget(self.NoButton)
        self.layout.addWidget(self.YesButton)
        self.BackGround.setLayout(self.layout)

    def UIfun(self):

        # 取消确定按钮
        def NO():
            self.fun_false()
            self.close()
            self.dad.ChildWindow = None
        self.NoButton.clicked.connect(NO)
        self.CloseButton.clicked.connect(NO)

        def YES():
            self.fun_true()
            self.close()
            self.dad.ChildWindow = None
        self.YesButton.clicked.connect(YES)

    def SetDay(self):
        temp_qss = DayQss
        self.Theme = "Day"
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
                                        border-radius: 30px;''' % (temp_qss.theme_color))
        # 显示的标题
        self.Marking.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 22))
        self.Marking.setText(QtCore.QCoreApplication.translate("MainWindow", "🥲"))
        self.Marking.setAlignment(Qt.AlignCenter)  # 对齐

        self.Text.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Text.setText(self.text)
        self.Text.setAlignment(Qt.AlignCenter)
        self.Text.setStyleSheet('''border: 0px;
                                        color:%s;''' % (temp_qss.font_color1))
        self.Text.setReadOnly(True)  # 设置QTextEdit为只读

        # 取小按钮
        self.NoButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.NoButton.setText(QtCore.QCoreApplication.translate("MainWindow", "取消"))
        self.NoButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.NoButton.setMinimumHeight(30)

        # 确定按钮
        self.YesButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.YesButton.setText(QtCore.QCoreApplication.translate("MainWindow", "确定"))
        self.YesButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.YesButton.setMinimumHeight(30)

        # 关闭
        self.CloseButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.CloseButton.setText(QtCore.QCoreApplication.translate("MainWindow", "×"))
        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

    def SetNight(self):
        temp_qss = NightQss
        self.Theme = "Night"
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
                                                border-radius: 30px;''' % (temp_qss.theme_color))
        # 显示的标题
        self.Marking.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 22))
        self.Marking.setText(QtCore.QCoreApplication.translate("MainWindow", "🥲"))
        self.Marking.setAlignment(Qt.AlignCenter)  # 对齐

        self.Text.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Text.setText(self.text)
        self.Text.setAlignment(Qt.AlignCenter)
        self.Text.setStyleSheet('''border: 0px;
                                    color:%s;''' % (temp_qss.font_color1))
        self.Text.setReadOnly(True)  # 设置QTextEdit为只读

        # 取小按钮
        self.NoButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.NoButton.setText(QtCore.QCoreApplication.translate("MainWindow", "取消"))
        self.NoButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.NoButton.setMinimumHeight(30)

        # 确定按钮
        self.YesButton.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.YesButton.setText(QtCore.QCoreApplication.translate("MainWindow", "确定"))
        self.YesButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.YesButton.setMinimumHeight(30)

        # 关闭
        self.CloseButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.CloseButton.setText(QtCore.QCoreApplication.translate("MainWindow", "×"))
        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

    def show(self):
        super(QuestionWindow, self).show()
        self.Text.myresize()

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()


if __name__ == "__main__":
    import sys
    def f1():
        print("t")
    def f2():
        print("f")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QuestionWindow("123", "<这个操作是不可逆转的>\n真的要删除 %2 吗？", f2, f1)  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程