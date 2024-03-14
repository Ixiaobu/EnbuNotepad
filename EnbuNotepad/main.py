import sqlite3

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton

import SQLopt
from AddClassWindow import AddClassWindow
from AddInfoWindow import AddInfoWindow
from AlertWindow import AlertWindow
from EnbuQt import ShowContainer, SearchInput, MoveButton, ShowClassName, \
    EmptBox, TextBox, LeftLayout, ShowContainerBar, AddClassButton
from ReadIni import AllQss, DayQss, NightQss
from ToolFun import GetTheme, RemoveLayoutItem
from ZEBqt import EnbuBasicWindow

'''
需要安装的库文件:
pip install pyinstaller
pip install pyqt5
pip install xlsxwriter
pip install Pillow
pip install chardet
'''
# pyinstaller -F -w -i G:\Management\data\ico\Logo3.ico main.py


# 主窗口类
class MainWindow(EnbuBasicWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.Theme = GetTheme(AllQss.default_mode)  # 储存深浅色
        self.conn = sqlite3.connect('data/test.db')
        self.setWindowIcon(QIcon("data/ico/Logo3.ico"))
        self.cur = self.conn.cursor()  # 数据库的指针
        self.now_class = None  # 当前显示的类别
        self.ChildWindow = None  # 记录子窗口
        self.resize(840, 640)  # 尺寸
        self.SetUp()

    def UIinit(self):
        self.BackGround  = QLabel('', self)         # 背景
        self.MiniButton  = QPushButton('', self)    # 最小化按钮
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.ResizeBtn   = MoveButton('', self)  # 缩放按钮

        self.TextBox = TextBox('', self)  # 左侧文本（一堆）
        self.ModButton   = QPushButton('', self)    # 深浅色切换按钮

        self.SearchIn    = SearchInput('', self)    # 搜索内容

        self.LeftMyLay   = LeftLayout('', self)     # 左侧布局
        self.ShowClass = ShowContainer('', self)  # 显示信息的框架
        self.UpdataClass()  # 加入表名

        self.Container = ShowContainerBar('', self)  # 显示信息的框架
        self.Container.UpdataContainer("根目录")  # 加入详细+内容

        self.AddButton = QPushButton('', self)  # 添加信息的按钮

    # 更新表名
    def UpdataClass(self):
        # 清空布局内的控件
        RemoveLayoutItem(self.ShowClass.layout)

        # 先把根目录加进去
        box_temp = ShowClassName('', self, [AllQss.text1, AllQss.text2, AllQss.text3, "", "", ""])
        box_temp.Clicked()   # 把灯亮起来
        self.now_class = box_temp  # 默认显示根目录
        self.ShowClass.layout.addWidget(box_temp)

        # 逐个加入各个表名
        for data in SQLopt.GetTableInfo(self.cur, "根目录")[1:]:
            box_temp = ShowClassName('', self, data)
            self.ShowClass.layout.addWidget(box_temp)
        self.Addclass = AddClassButton('', self)  # 增加一个表的按钮
        self.ShowClass.layout.addWidget(self.Addclass)

        self.ShowClass.layout.addWidget(EmptBox('', self))  # 加入一个空的控件
        QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if GetTheme(self.Theme) == "Day" else NightQss

        # 背景
        self.BackGround.setStyleSheet('''background-color: %s ;
                                        border: 1px solid %s;
                                        border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))
        self.BackGround.setGraphicsEffect(self.Get_Shaow())

        # 最小化按钮
        self.MiniButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.MiniButton.setText(QtCore.QCoreApplication.translate("MainWindow", "-"))
        self.MiniButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

        # 关闭
        self.CloseButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.CloseButton.setText(QtCore.QCoreApplication.translate("MainWindow", "×"))
        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

        # 缩放
        self.ResizeBtn.setText("⇲")
        self.ResizeBtn.setFont(QtGui.QFont("arial", AllQss.font_size + 15))
        self.ResizeBtn.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color2))

        # 深浅色切换按钮
        self.ModButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 1px solid %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s}''' %
            (temp_qss.color1, temp_qss.color2, temp_qss.color2, temp_qss.color1))

        # 添加信息
        self.AddButton.setFont(QtGui.QFont("arial", AllQss.font_size + 40))
        self.AddButton.setText(QtCore.QCoreApplication.translate("MainWindow", "+"))
        self.AddButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.AddButton.setGraphicsEffect(self.Get_Shaow())

    def UIsite(self):
        # 背景
        k = 25  # 边距变量
        self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))

        # 最小化按钮
        self.MiniButton.setGeometry(QtCore.QRect(self.width() - 75 - k, k - 7, 30, 30))

        # 关闭
        self.CloseButton.setGeometry(QtCore.QRect(self.width() - 45 - k, k - 5, 30, 30))

        # 深浅色切换按钮
        self.ModButton.setGeometry(QtCore.QRect(k + 10, k + 10, 80, 14))

        # 缩放
        self.ResizeBtn.setGeometry(QtCore.QRect(self.width() - 37 - k, self.height() - 37 - k, 30, 30))

        # 搜索内容
        self.SearchIn.setGeometry((k + 190, k + 35, 575, 35))

        # 左侧布局
        self.LeftMyLay.setGeometry(QtCore.QRect(k + 2, k + 25, 200, 520))
        self.LeftMyLay.layout.addWidget(self.TextBox)
        self.LeftMyLay.layout.addWidget(self.ShowClass)
        self.ShowClass.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 类型框框 关掉滚动条

        # 详细框框
        self.Container.setGeometry(QtCore.QRect(k + 185, k + 70, 595, 490))

        # 添加信息按钮
        self.AddButton.setGeometry(QtCore.QRect(self.width() - 100 - k, self.height() - 110 - k, 60, 60))

    def UIfun(self):
        # 关闭按钮
        def ClossAll():
            self.cur.close()  # 关闭
            self.conn.close()  # 关闭
            SQLopt.CopySql()  # 保存历史版本
            self.close()
            sys.exit()
        self.CloseButton.clicked.connect(ClossAll)

        # 最小按钮
        self.MiniButton.clicked.connect(lambda x: self.showMinimized())

        # 切换模式
        def ChangMod():
            if self.Theme == "Day":
                self.Theme = "Night"
                self.SearchIn.SetNight()   # 搜索框
                self.ShowClass.SetNight()  # 类型框框
                self.Container.SetNight()  # 详细框框
                self.TextBox.SetNight()    # 文本
                if self.ChildWindow != None:
                    self.ChildWindow.SetNight()  # 子窗口
                    self.ChildWindow.activateWindow()
            else:
                self.Theme = "Day"
                self.SearchIn.SetDay()   # 搜索框
                self.ShowClass.SetDay()  # 类型框框
                self.Container.SetDay()  # 详细框框
                self.TextBox.SetDay()    # 文本
                if self.ChildWindow != None:
                    self.ChildWindow.SetDay()  # 子窗口
                    self.ChildWindow.activateWindow()


            # 根据深浅色选择一个配置
            temp_qss = DayQss if GetTheme(self.Theme) == "Day" else NightQss

            # 背景
            self.BackGround.setStyleSheet('''background-color: %s ;
                                            border: 1px solid %s;
                                            border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))

            # 最小化按钮
            self.MiniButton.setStyleSheet(
                '''QPushButton{background:rgb(0,0,0,0);color:%s}
                QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
                (temp_qss.font_color1))

            # 关闭
            self.CloseButton.setStyleSheet(
                '''QPushButton{background:rgb(0,0,0,0);color:%s}
                QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
                (temp_qss.font_color1))

            # 缩放
            self.ResizeBtn.setStyleSheet(
                '''QPushButton{background:rgb(0,0,0,0);color:%s}
                QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
                (temp_qss.font_color2))

            # 深浅色切换按钮
            self.ModButton.setStyleSheet(
                '''QPushButton{background:%s;border-radius: 7px;border: 1px solid %s;}
                QPushButton:hover{background:%s;border-radius: 7px;border: 1px solid %s}''' %
                (temp_qss.color1, temp_qss.color2, temp_qss.color2, temp_qss.color1))

            # 添加按钮
            self.AddButton.setStyleSheet(
                '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;}
                QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;}''' %
                (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

        self.ModButton.clicked.connect(ChangMod)

        # 缩放界面
        def ResizeWindow():
            k = 25
            w, h = self.ResizeBtn.x() + k + 35, self.ResizeBtn.y() + k + 35
            self.resize(w, h) # 总窗口尺寸

            self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))
            self.MiniButton.setGeometry(QtCore.QRect(self.width() - 75 - k, k - 7, 30, 30))  # 最小化按钮
            self.CloseButton.setGeometry(QtCore.QRect(self.width() - 45 - k, k - 5, 30, 30))  # 关闭
            self.AddButton.setGeometry(QtCore.QRect(self.width() - 100 - k, self.height() - 110 - k, 60, 60))
            # 窗口太小就只显示详细内容
            if w < int(AllQss.resize_threshold):
                self.SearchIn.setGeometry((k + 7, k + 35, self.width() - 50 - 23, 35))  # 搜索内容
                self.LeftMyLay.setGeometry(QtCore.QRect(k + 2, k + 40, 0, self.height() - 120))  # 显示左边布局
                self.Container.setGeometry(QtCore.QRect(k + 2, k + 70, self.width() - 50 - 4, self.height() - 150))  # 显示信息的框架
            else:
                self.SearchIn.setGeometry((k + 190, k + 35, self.width() - 265, 35))  # 搜索内容
                self.LeftMyLay.setGeometry(QtCore.QRect(k + 2, k + 40, 200, self.height() - 120))  # 显示左边布局
                self.Container.setGeometry(QtCore.QRect(k + 185, k + 70, self.width() - 245, self.height() - 150))  # 显示信息的框架

        self.ResizeBtn.siteChanged.connect(ResizeWindow)

        # 添加一个类
        def AddClassfun():
            # 如果仍有子窗口打开，也放弃操作
            if self.Container.DispalyIndoWindowList:
                for window in self.Container.DispalyIndoWindowList:
                    window.activateWindow()
                AlertWindow(self, "🤐", "您当前仍在编辑\n<%s>\n请完成编辑后再切换主题" % self.now_class.name).show()
                return

            if self.ChildWindow == None:
                # 先清空容器，省的bug
                self.Container.RemoveItem()

                # 子窗口
                AddClassWindow_ = AddClassWindow(self)  # 添加类别
                AddClassWindow_.show()
                self.ChildWindow = AddClassWindow_
            else:
                self.ChildWindow.activateWindow()
        self.Addclass.clicked.connect(AddClassfun)

        # 添加信息
        def AddInfo():
            if self.ChildWindow == None:
                # 如果在根目录打开就提示一下
                if self.now_class.name == AllQss.text1:
                    AlertWindow(self, "🥱", "<您当前在根目录>\n\n想添加新的主题请点击\n界面左端加号\n").show()
                    return
                # 如何还需要密码也提示一下
                if self.now_class.kind == "close":
                    def true_add():
                        AddWindow_ = AddInfoWindow("", self)
                        AddWindow_.show()
                        self.ChildWindow = AddWindow_
                    self.now_class.mouseLeftClick(fun_true_add=true_add)
                    return

                AddWindow_ = AddInfoWindow("", self)
                AddWindow_.show()
                self.ChildWindow = AddWindow_
            else:
                self.ChildWindow.activateWindow()

        self.AddButton.clicked.connect(AddInfo)

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

if __name__ == "__main__":
    import sys
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程