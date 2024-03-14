import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QLineEdit

from ReadIni import AllQss, DayQss, NightQss
from ToolFun import LimitStrLen
from ZEBqt import EnbuBasicWindow


# 主窗口类
class PassWordWindow(EnbuBasicWindow):
    def __init__(self, dad, password, fun_false, fun_true):
        super(PassWordWindow, self).__init__()
        self.Theme = dad.Theme  # 储存深浅色
        self.dad = dad
        self.password = password
        self.fun_false = fun_false
        self.fun_true = fun_true
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 设置窗口浮在最上方
        self.resize(400, 250)  # 尺寸
        self.SetUp()

    def UIinit(self):
        self.BackGround  = QLabel('', self)         # 背景
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.Marking     = QLabel('', self)         # 标记文本
        self.PassWordInput   = QLineEdit('', self)  # 密码输入框
        self.PassWordFinish  = QPushButton('', self)  # 完成确定

        self.text1 = QLabel('', self)  # 文本1
        self.text2 = QLabel('', self)  # 文本2

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
        self.Marking.setText(QtCore.QCoreApplication.translate("MainWindow", "🙈"))
        self.Marking.setAlignment(Qt.AlignCenter)  # 对齐

        # 文本
        self.text1.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 14))
        self.text1.setText(QtCore.QCoreApplication.translate("MainWindow", "%s 的密码:" % (LimitStrLen(self.dad.now_class.name, 7))))
        self.text1.setStyleSheet('''color:%s;border: 0px;''' % (temp_qss.font_color1))

        # 密码
        self.PassWordInput.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.PassWordInput.setAlignment(Qt.AlignCenter)
        self.PassWordInput.setStyleSheet('''background-color: %s ;
                                        border: 0px;
                                        color:%s;
                                        padding: 5px;''' % (temp_qss.fill_color1, temp_qss.font_color1))
        self.PassWordInput.setEchoMode(QLineEdit.Password) # 设置输入是密码格式

        # 完成按钮
        self.PassWordFinish.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.PassWordFinish.setText(QtCore.QCoreApplication.translate("MainWindow", "打开"))
        self.PassWordFinish.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.PassWordFinish.setMinimumHeight(30)
        self.PassWordFinish.setMinimumWidth(150)
        self.PassWordFinish.setMaximumWidth(150)

        # 文本
        self.text2.setFont(QtGui.QFont("arial", AllQss.font_size + 10))
        self.text2.setText(QtCore.QCoreApplication.translate("MainWindow", ""))
        self.text2.setStyleSheet('''color:%s;border: 0px;''' % ("rgb(244,71,53)"))

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
        self.layout.addWidget(self.text1)
        self.layout.addWidget(self.PassWordInput)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.PassWordFinish, 1, Qt.AlignHCenter)
        self.BackGround.setLayout(self.layout)

    def UIfun(self):
        # 关闭按钮
        def ClossAll():
            self.fun_false()
            self.dad.ChildWindow = None
            self.close()
        self.CloseButton.clicked.connect(ClossAll)

        # 完成按钮
        def Finish():
            if self.PassWordInput.text() == self.password:
                self.close()
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
                self.dad.now_class.kind = "open"
                self.dad.ChildWindow = None
                self.fun_true()
            else:
                self.text2.setText("密码错误")

        self.PassWordInput.editingFinished.connect(Finish)
        self.PassWordFinish.clicked.connect(Finish)

    def SetDay(self):
        temp_qss = DayQss
        self.Theme = "Day"
        # 背景
        self.BackGround.setStyleSheet('''background-color: %s ;
                                        border: 1px solid %s;
                                        border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))

        # 标记文本
        self.Marking.setStyleSheet('''background-color: %s ;
                                        border: 0px;
                                        color:#ffffff;
                                        border-radius: 30px;''' % (temp_qss.theme_color))

        # 文本
        self.text1.setStyleSheet('''color:%s;border: 0px;''' % (temp_qss.font_color1))

        # 密码
        self.PassWordInput.setStyleSheet('''background-color: %s ;
                                        border: 0px;
                                        color:%s;
                                        padding: 5px;''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 完成按钮
        self.PassWordFinish.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, temp_qss.font_color1, temp_qss.theme_color, temp_qss.font_color1, "#ffffff"))

        # 文本
        self.text2.setStyleSheet('''color:%s;border: 0px;''' % ("rgb(244,71,53)"))

        # 关闭
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

        # 标记文本
        self.Marking.setStyleSheet('''background-color: %s ;
                                        border: 0px;
                                        color:#ffffff;
                                        border-radius: 30px;''' % (temp_qss.theme_color))

        # 文本
        self.text1.setStyleSheet('''color:%s;border: 0px;''' % (temp_qss.font_color1))

        # 密码
        self.PassWordInput.setStyleSheet('''background-color: %s ;
                                        border: 0px;
                                        color:%s;
                                        padding: 5px;''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 完成按钮
        self.PassWordFinish.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, temp_qss.font_color1, temp_qss.theme_color, temp_qss.font_color1, "#ffffff"))

        # 文本
        self.text2.setStyleSheet('''color:%s;border: 0px;''' % ("rgb(244,71,53)"))

        # 关闭
        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

    def show(self):
        if self.dad.ChildWindow == None:
            self.dad.ChildWindow = self
            super(PassWordWindow, self).show()
        else:
            self.dad.ChildWindow.activateWindow()

    # 高亮
    def activateWindow(self):
        super(PassWordWindow, self).activateWindow()
        for _ in range(2):
            self.Marking.setText("🙊")
            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
            time.sleep(0.05)
            self.Marking.setText("🙉")
            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
            time.sleep(0.05)
            self.Marking.setText("🙈")
            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
            time.sleep(0.05)

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = PassWordWindow("", "123", "✅", "请")  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程