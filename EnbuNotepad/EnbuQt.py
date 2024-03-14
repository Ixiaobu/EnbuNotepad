from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QCoreApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QComboBox, QToolTip, QWidget, QVBoxLayout, QScrollArea, \
    QLineEdit, QMenu, QAction

import SQLopt
from AlertWindow import AlertWindow
from DisPlayClassInfo import DisPlayClassInfo
from DisplayInfoWindow import DisplayInfoWindow
from PassWordWindow import PassWordWindow
from QuestionWindow import QuestionWindow
from ReadIni import AllQss, DayQss, NightQss
from ToolFun import GetTheme, IsGoodImg, GetImg, RemoveLayoutItem


# 类模板
class Name():
    def __init__(self, name, dad):
        super(Name, self).__init__(name, dad)
        self.SetUp()

    def UIinit(self):
        pass

    def UIcss(self):
        # 背景
        self.setStyleSheet('''background-color: rgb(240, 240, 240);
                              border-radius: 3px;
                              border: 1px solid #c5c5c5; /* 边框色 */''')

    def SetDay(self):
        pass

    def SetNight(self):
        pass

    def SetUp(self):
        self.UIinit()
        self.UIcss()

# 缩放按钮
class MoveButton(QPushButton):
    siteChanged = pyqtSignal(str)

    def __init__(self, name, dad):
        super(MoveButton, self).__init__(dad)
        self.dad = 0
        self.m_flag = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):

        if Qt.LeftButton and self.m_flag:
            try:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                if self.x() < 200 or self.y() < 400:
                    x = max(self.x(), 201)
                    y = max(self.y(), 401)
                    self.move(x, y)

                QMouseEvent.accept()
                self.siteChanged.emit("0")
                self.change_window_emit(self.x(), self.y())
            except:
                return

# 圆角输入控件
class SearchInput(QLabel):
    def __init__(self, name, dad):
        self.dad = dad
        self.Theme = self.dad.Theme
        super(SearchInput, self).__init__(name, dad)
        self.SetUp()

    def UIinit(self):
        self.Input = QLineEdit('', self)  # 输入
        self.Button = QPushButton('', self)  # 逆序按钮

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if GetTheme(AllQss.default_mode) == "Day" else NightQss
        # 输入
        self.Input.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Input.setStyleSheet('''background-color: %s;
                                    border: 1px solid %s;
                                    color: %s''' % (temp_qss.fill_color1, temp_qss.fill_color1, temp_qss.font_color1))

        self.Button.setText("⇅")
        self.Button.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 17))
        self.Button.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s;border: 0px}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s;border: 0px}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

    def UIfun(self):
        def FindInput():
            # 如何还需要密码也提示一下
            if self.dad.now_class.kind == "close":
                def true_add():
                    data = SQLopt.SelectSql(self.dad.cur, self.dad.now_class.name if self.dad.now_class.name != AllQss.text1 else "根目录", input)
                    self.dad.Container.UpdataContainerFromData(data)
                self.dad.now_class.mouseLeftClick(fun_true_add=true_add)
                return

            # 如果当前有其他窗口则放弃操作
            if self.dad.ChildWindow != None:
                self.dad.ChildWindow.activateWindow()
                AlertWindow(self, "🤐", "您当前仍在编辑\n<%s>\n请完成编辑后再进行搜索" % self.dad.now_class.name).show()
                return

            data = SQLopt.SelectSql(self.dad.cur,
                                   self.dad.now_class.name if self.dad.now_class.name != AllQss.text1 else "根目录",
                                    self.Input.text())
            self.dad.Container.UpdataContainerFromData(data)

        self.Input.editingFinished.connect(FindInput)

        def ReverseData():
            self.dad.Container.info.reverse()  # 反转
            self.dad.Container.UpdataContainerFromData(self.dad.Container.info)


        self.Button.clicked.connect(ReverseData)

    # 尺寸调整
    def setGeometry(self, site):
        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.Theme) == "Day" else NightQss

        x, y, w, h  = site
        self.resize(w, h)
        self.move(x, y)
        self.setStyleSheet('''background-color: %s;
                              border-radius: %dpx;
                              border: 1px solid %s;''' % (temp_qss.fill_color1, min(w // 2, h // 2), temp_qss.stroke_color1))
        # 输入框
        self.Input.setStyleSheet('''background-color: %s;
                                    border: 1px solid %s;
                                    color: %s''' % (temp_qss.fill_color1, temp_qss.fill_color1, temp_qss.font_color1))

        k = 5
        self.Input.setGeometry(QtCore.QRect(h//2, k, w - h - h//2, h - 2*k))
        self.Button.setGeometry(QtCore.QRect(h // 2 + w - h - h//2, 0, h, h))


    def SetDay(self):
        self.Theme = "Day"
        # 本体
        h = self.height()
        self.setStyleSheet('''background-color: %s;
                                      border-radius: %dpx;
                                      border: 1px solid %s;''' % (DayQss.fill_color1, h // 2, DayQss.stroke_color1))

        # 输入
        self.Input.setStyleSheet('''background-color: %s;
                                            border: 1px solid %s;
                                            color: %s''' % (DayQss.fill_color1, DayQss.fill_color1, DayQss.font_color1))

        self.Button.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s;border: 0px}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s;border: 0px}''' %
            (DayQss.font_color1, DayQss.theme_color))


    def SetNight(self):
        self.Theme = "Night"

        w = self.width()
        h = self.height()
        self.setStyleSheet('''background-color: %s;
                                      border-radius: %dpx;
                                      border: 1px solid %s;''' % (NightQss.fill_color1, min(w // 2, h // 2), NightQss.stroke_color1))
        # 输入
        self.Input.setStyleSheet('''background-color: %s;
                                                    border: 1px solid %s;
                                                    color: %s''' % (NightQss.fill_color1, NightQss.fill_color1, NightQss.font_color1))

        self.Button.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s;border: 0px}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s;border: 0px}''' %
            (NightQss.font_color1, NightQss.theme_color))


    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIfun()

# 一个正方形的lable
class SquareLabel(QLabel):
    def resizeEvent(self, event):
        size = min(event.size().width(), event.size().height())
        self.setFixedSize(size, size)
        super().resizeEvent(event)

# 用来平衡留白的空控件
class EmptBox(QLabel):
    def __init__(self, name, dad, text=""):
        super(EmptBox, self).__init__(name, dad)
        self.dad = dad
        self.setMinimumSize(100, 80)  # 设置输入的最小尺寸
        self.text = text
        self.UIcss()

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if self.dad.Theme == "Day" else NightQss
        # 设置文本格式
        self.setText(self.text)
        self.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.setStyleSheet("color: %s;"
                             "border: 0px" % temp_qss.font_color1)
        self.setAlignment(Qt.AlignCenter)

    def SetDay(self):
        self.setStyleSheet("color: %s;"
                           "border: 0px" % DayQss.font_color1)

    def SetNight(self):
        self.setStyleSheet("color: %s;"
                           "border: 0px" % NightQss.font_color1)

# 用来显示文字的容器
class TextBox(QLabel):
    def __init__(self, name, dad):
        self.dad = dad
        self.Theme = self.dad.Theme
        super(TextBox, self).__init__(name, dad)
        self.SetUp()

    def UIinit(self):
        # 一些文本
        self.text1 = QLabel('', self)  # 第一个大字标题
        self.text2 = QLabel('', self)  # 第二个时间信息
        self.text3 = QLabel('', self)  # 第三个内容描述
        self.layout = QVBoxLayout()    # 纵向布局

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if GetTheme(self.dad.Theme) == "Day" else NightQss

        # 一些文本
        self.text1.setText(AllQss.text1)
        self.text1.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 22))
        self.text1.setWordWrap(True)  # 自动换行
        self.text1.setStyleSheet("font-weight: bold;color: %s" % temp_qss.theme_color)

        self.text2.setText(AllQss.text2)
        self.text2.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 12))
        self.text2.setWordWrap(True)  # 自动换行
        self.text2.setStyleSheet("color: %s" % temp_qss.font_color1)

        self.text3.setText(AllQss.text3)
        self.text3.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 13))
        self.text3.setWordWrap(True)  # 自动换行
        self.text3.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)  # 自动对齐
        self.text3.setStyleSheet("color: %s" % temp_qss.font_color1)

    def UIsite(self):
        self.layout.addWidget(self.text1)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.text3)
        self.setLayout(self.layout)

    def SetDay(self):
        self.Theme = "Day"
        self.text1.setStyleSheet("font-weight: bold;color: %s" % DayQss.theme_color)
        self.text2.setStyleSheet("color: %s" % DayQss.font_color1)
        self.text3.setStyleSheet("color: %s" % DayQss.font_color1)

    def SetNight(self):
        self.Theme = "Night"
        self.text1.setStyleSheet("font-weight: bold;color: %s" % NightQss.theme_color)
        self.text2.setStyleSheet("color: %s" % NightQss.font_color1)
        self.text3.setStyleSheet("color: %s" % NightQss.font_color1)

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()

# 横向展示的表名控件
class ShowClassName(QLabel):

    def __init__(self, name, dad, data):
        super(ShowClassName, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.data = data
        self.name = data[0]  # 显示的名字
        self.create_time = data[1]  # 创建时间
        self.remarks = data[2]  # 备注
        self.password = data[4]  # 密码
        self.kind = "close"
        self.SetUp()

    def UIinit(self):
        self.layoutText = QVBoxLayout()  # 纵向布局
        self.layout    = QHBoxLayout()  # 横向布局
        self.NameLable = QLabel('', self)  # 显示名字的控件
        self.Light     = QLabel('', self)  # 选中指示灯
        self.layoutTextBox = QLabel('', self)  # 放置文本布局
        self.PageText  = QLabel('', self)  # 页码文本

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.Theme) == "Day" else NightQss

        self.layoutText.setContentsMargins(0, 0, 0, 0)  # 设置边距为0

        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;''' % (temp_qss.fill_color1))
        self.setMinimumSize(100, 60)  # 设置输入的最小尺寸
        self.setMaximumSize(1000000, 200)  # 设置输入的最小尺寸

        # 灯泡
        self.Light.setStyleSheet('''background-color: rgba(0,0,0,0);
                                    border: 1px solid rgba(0,0,0,0);''')
        self.Light.setMinimumSize(10, 20)  # 设置输入的最小尺寸
        self.Light.setMaximumSize(10, 60)  # 设置输入的最小尺寸

        # 名字
        self.NameLable.setText(self.name)
        self.NameLable.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 18))
        self.NameLable.setWordWrap(True)  # 自动换行
        self.NameLable.setStyleSheet("font-weight: bold;"
                                     "color: %s;"
                                     "border: 1px solid rgba(0,0,0,0)" % (temp_qss.font_color1))
        # 防止文本布局
        self.layoutTextBox.setStyleSheet('''background-color: rgba(0,0,0,0);
                                    border: 1px solid rgba(0,0,0,0);''')

        # 页码
        self.PageText.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 11))
        self.PageText.setStyleSheet("background-color: rgba(0,0,0,0);"
                                    "color: %s;"
                                     "border: 1px solid rgba(0,0,0,0)" % (temp_qss.font_color1))

    def UIsite(self):
        self.layoutText.addWidget(self.NameLable)
        self.layoutTextBox.setLayout(self.layoutText)

        self.layout.addWidget(self.Light)
        self.layout.addWidget(self.layoutTextBox)
        self.setLayout(self.layout)

    def UIfun(self):
        self.setContextMenuPolicy(3)  # 设置右击菜单策略为CustomContextMenu
        self.customContextMenuRequested.connect(self.showContextMenu)

    # 右键窗口
    def showContextMenu(self, pos):
        temp_qss = DayQss if self.Theme == "Day" else NightQss
        self.Clicked()

        # 如果当前在根目录，也放弃操作
        if self.dad.now_class.name == AllQss.text1:
            return

        # 如果当前有其他窗口则放弃操作
        if self.dad.ChildWindow != None:
            self.dad.ChildWindow.activateWindow()
            return

        # 如果仍有子窗口打开，也放弃操作
        if self.dad.Container.DispalyIndoWindowList:
            for window in self.dad.Container.DispalyIndoWindowList:
                window.activateWindow()
            AlertWindow(self, "🤐", "您当前仍在编辑\n<%s>\n请完成编辑后再切换主题" % self.dad.now_class.name).show()
            return


        # 右键窗口
        def RightWindowOpen():
            # 右键菜单
            menu = QMenu(self)
            menu.setStyleSheet(
                "QMenu { background-color: %s; color: %s; border: 1px solid %s;border-radius: 5px; padding: 5px}"
                "QMenu::item:selected { background-color: %s; color: %s; border: 1px solid %s;border-radius: 5px; padding: 5px}"
                % (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.stroke_color1,
                   temp_qss.select_fill_color, temp_qss.font_color1, temp_qss.stroke_color1))  # 设置弹窗的样式表
            menu.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 12))  # 设置弹窗的字体
            menu.setMaximumWidth(80)  # 设置最大宽度为100像素

            action1 = QAction(QIcon(r"data\ico\ico1.png"), "上移", self)
            action2 = QAction(QIcon(r"data\ico\ico2.png"), "下移", self)
            action3 = QAction(QIcon(r"data\ico\ico3.png"), "编辑", self)
            action4 = QAction(QIcon(r"data\ico\ico4.png"), "另存", self)
            action5 = QAction(QIcon(r"data\ico\ico5.png"), "删除", self)
            menu.addAction(action1)
            menu.addAction(action2)
            # 在QMenu中加入一个分割线
            menu.addSeparator()
            menu.addAction(action3)
            menu.addAction(action4)
            menu.addAction(action5)

            action = menu.exec_(self.mapToGlobal(pos))
            if action == action1:
                # 上移操作
                temp_layout = self.dad.ShowClass.layout
                index = temp_layout.indexOf(self.dad.now_class)
                if index > 1:
                    temp_layout.insertWidget(index - 1, self)
                    SQLopt.ExchangeTwoRow(self.dad.conn, self.dad.cur, "根目录",
                                          temp_layout.itemAt(index).widget().data,
                                          temp_layout.itemAt(index - 1).widget().data)

            elif action == action2:
                temp_layout = self.dad.ShowClass.layout
                index = temp_layout.indexOf(self)
                if index < temp_layout.count() - 3:
                    temp_layout.insertWidget(index + 1, self)
                    SQLopt.ExchangeTwoRow(self.dad.conn, self.dad.cur, "根目录",
                                          temp_layout.itemAt(index).widget().data,
                                          temp_layout.itemAt(index + 1).widget().data)

            elif action == action3:
                # 先清空容器，省的bug
                self.dad.Container.RemoveItem()
                DisPlayClassInfo('', self.dad, self.data).show()

            elif action == action4:
                # 如果保存成功了
                if SQLopt.SaveSqlAsExcel(self.dad.cur, self.name):
                    AlertWindow(self.dad, "😘", "<%s>\n已保存至:SavedFile/%s.xlsx" % (self.name, self.name)).show()
                else:
                    AlertWindow(self.dad, "🤯", "<保存失败了>\n我也不知道为什么，请尝试重启App").show()

            elif action == action5:
                def fun_true():
                    # 从布局中移除要删除的控件
                    self.dad.ShowClass.layout.removeWidget(self)
                    self.setVisible(False)  # 隐藏控件
                    # 从数据库中删除
                    SQLopt.DeleteTable(self.dad.conn, self.dad.cur, self.name)
                    # 清空布局内的控件
                    self.dad.Container.RemoveItem()

                QuestionWindow(self.dad, "🥲", "<这个操作是不可逆转的>\n真的要删除 %s 吗？" % self.name,
                               lambda :None, fun_true).show()


        # 让窗口显示内容
        def Updata():
            self.dad.Container.UpdataContainer(self.name if self.name != AllQss.text1 else "根目录")
            RightWindowOpen()

        # 用户点了错号
        def fun_false():
            # 清空布局内的控件
            self.dad.Container.RemoveItem()
            self.dad.Container.info = []

        # 如果还没有打开过
        if self.kind != "open" and self.password:
            PassWordWindow(self.dad, self.password, fun_false, Updata).show()
        else:
            Updata()

    def SetDay(self):
        self.Theme = "Day"
        # 背景
        self.setStyleSheet('''background-color: %s;
                                      border-radius: 7px;''' % (DayQss.fill_color1))
        # 名字
        self.NameLable.setStyleSheet("font-weight: bold;"
                                     "color: %s;"
                                     "border: 1px solid rgba(0,0,0,0)" % (DayQss.font_color1))
        # 页码
        self.PageText.setStyleSheet("background-color: rgba(0,0,0,0);"
                                    "font-weight: bold;"
                                     "color: %s;"
                                     "border: 1px solid rgba(0,0,0,0)" % (DayQss.font_color1))

        # 灯泡
        if self.dad.now_class == self:
            # 显示亮起的灯
            self.Light.setStyleSheet('''background-color: %s;
                                border-radius: 2px;
                                border: 1px solid rgba(0,0,0,0);''' % (DayQss.theme_color))

    def SetNight(self):
        self.Theme = "Night"
        # 背景
        self.setStyleSheet('''background-color: %s;
                                      border-radius: 7px;''' % (NightQss.fill_color1))
        # 名字
        self.NameLable.setStyleSheet("font-weight: bold;"
                                     "color: %s;"
                                     "border: 1px solid rgba(0,0,0,0)" % (NightQss.font_color1))
        # 页码
        self.PageText.setStyleSheet("background-color: rgba(0,0,0,0);"
                                    "font-weight: bold;"
                                    "color: %s;"
                                    "border: 1px solid rgba(0,0,0,0)" % (NightQss.font_color1))
        # 灯泡
        if self.dad.now_class == self:
            # 显示亮起的灯
            self.Light.setStyleSheet('''background-color: %s;
                                border-radius: 2px;
                                border: 1px solid rgba(0,0,0,0);''' % (NightQss.theme_color))

    # 监听鼠标悬浮事件
    def enterEvent(self, event):
        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.Theme) == "Day" else NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;''' % (temp_qss.select_fill_color))
        event.accept()

    # 监听鼠标离开事件
    def leaveEvent(self, event):
        # 获取主题色
        temp_qss = DayQss if self.Theme == "Day" else NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;''' % (temp_qss.fill_color1))
        event.accept()

    # 监听鼠标点击事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                self.mouseLeftClick()
            except:
                AlertWindow(self, "🤯", "\n<%s 打开失败>\n请尝试从历史版本中恢复数据" % self.name).show()


    # 左键调用函数
    def mouseLeftClick(self, fun_true_add=lambda:None , fun_false_add=lambda:None):
        # 如果当前有其他窗口则放弃操作
        if self.dad.ChildWindow != None:
            self.dad.ChildWindow.activateWindow()
            return

        # 如果仍有子窗口打开，也放弃操作
        if self.dad.Container.DispalyIndoWindowList:
            for window in self.dad.Container.DispalyIndoWindowList:
                window.activateWindow()
            AlertWindow(self, "🤐", "您当前仍在编辑\n<%s>\n请完成编辑后再切换主题" % self.dad.now_class.name).show()
            return

        # 清空布局内的控件
        self.dad.Container.RemoveItem()
        self.dad.Container.info = []
        self.Clicked()

        # 密码对了
        def fun_true():
            # 更新主窗口的内容
            self.dad.Container.UpdataContainer(self.name if self.name != AllQss.text1 else "根目录")
            fun_true_add()

        # 用户点了错号
        def fun_false():
            fun_false_add()

        # 如果有密码，判断一下
        if self.password and self.kind != "open":
            PassWordWindow(self.dad, self.password, fun_false, fun_true).show()
        else:
            self.dad.Container.UpdataContainer(self.name if self.name != AllQss.text1 else "根目录")
            self.kind = "open"

    # 被更改后，更新的方法
    def UpData(self, data):
        self.data = data
        self.name = data[0]  # 显示的名字
        self.create_time = data[1]  # 创建时间
        self.remarks = data[2]  # 备注
        self.password = data[4]  # 密码

        # 更新主窗口的文本
        self.dad.TextBox.text1.setText(self.name)
        self.dad.TextBox.text2.setText(self.create_time)
        self.dad.TextBox.text3.setText(self.remarks)

        # 清空布局内的控件
        self.dad.Container.RemoveItem()
        self.dad.Container.info = []
        self.Clicked()

        self.dad.Container.UpdataContainer(self.name if self.name != AllQss.text1 else "根目录")
        self.kind = "open"

    # 被点击时调用的东西
    def Clicked(self):
        # 防止重复点击同一个
        if self.dad.now_class == self:
            return

        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.Theme) == "Day" else NightQss

        # 更新主窗口的文本
        self.dad.TextBox.text1.setText(self.name)
        self.dad.TextBox.text2.setText(self.create_time)
        self.dad.TextBox.text3.setText(self.remarks)

        # 显示亮起的灯
        self.Light.setStyleSheet('''background-color: %s;
                            border-radius: 2px;
                            border: 1px solid rgba(0,0,0,0);''' % (temp_qss.theme_color))
        # 加入页码
        self.layoutText.addWidget(self.PageText)
        self.PageText.setText(" 00 / 00")

        if self.dad.now_class:
            self.dad.now_class.NotClicked() # 把旧的灯灭下去

        self.dad.now_class = self

    # 别人被点击时调用的东西
    def NotClicked(self):
        temp_qss = DayQss if self.Theme == "Day" else NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;''' % (temp_qss.fill_color1))
        # 显示没有灯
        self.Light.setStyleSheet('''background-color: rgba(0,0,0,0);
                            border-radius: 2px;
                            border: 1px solid rgba(0,0,0,0);''')

        # 删除页码显示
        self.layoutText.removeWidget(self.PageText)
        self.PageText.setText("")

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

# 增加表的按钮
class AddClassButton(QPushButton):
    def __init__(self, name, dad):
        super(AddClassButton, self).__init__(name, dad)
        self.dad = dad
        self.SetUp()

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.Theme) == "Day" else NightQss

        self.setFont(QtGui.QFont("arial", AllQss.font_size + 40))
        self.setText(QtCore.QCoreApplication.translate("MainWindow", "+"))
        self.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 0px;color: %s;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.select_fill_color, temp_qss.font_color1))

    def UIfun(self):
        pass

    def SetDay(self):
        self.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 0px;color: %s;}''' %
            (DayQss.fill_color1, DayQss.font_color1, DayQss.select_fill_color, DayQss.font_color1))

    def SetNight(self):
        self.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 0px;color: %s;}''' %
            (NightQss.fill_color1, NightQss.font_color1, NightQss.select_fill_color, NightQss.font_color1))

    def SetUp(self):
        self.UIcss()
        self.UIfun()

# 横向展示的框框详细
class ShowLine(QLabel):
    def __init__(self, name, dad, data):
        self.dad = dad
        self.Theme = self.dad.Theme
        self.data = data
        self.id = 0
        self.DisPlayWindow = None  # 记录详细展示的窗口有没有打开
        self.newDisplay = DisplayInfoWindow('', self, self.data)  # 展示窗口

        super(ShowLine, self).__init__(name, dad)
        self.SetUp()

    def UIinit(self):
        self.ImgShow   = SquareLabel('', self)  # 显示图片
        self.NameLable = QLabel('', self)  # 显示名字
        self.TextShow1 = QLabel('', self)  # 第一个信息
        self.TextBox   = QLabel('', self)  # 一个容器
        self.Textlayout= QVBoxLayout()     # 创建一个垂直布局
        self.layout    = QHBoxLayout()  # 创建一个横向布局

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if self.Theme == "Day" else NightQss
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;
                              border: 0px''' % (temp_qss.fill_color1))
        self.setMinimumSize(100, 80)  # 设置输入的最小尺寸
        self.setMaximumSize(1000000, 200)  # 设置输入的最da尺寸

        # 把不需要显示的边框去掉
        self.TextBox.setStyleSheet("border: 0px")
        self.ImgShow.setStyleSheet("background-color: rgba(0,0,0,0);border: 0px")
        self.ImgShow.setScaledContents(True)  # 图片大小自适应

        # 设置文本格式
        self.NameLable.setText(self.data[0])
        self.NameLable.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 18))
        self.NameLable.setStyleSheet("font-weight: bold;"
                                     "color: %s;"
                                     "border: 0px solid rgba(0,0,0,0)" % temp_qss.font_color1)
        self.NameLable.setWordWrap(True)  # 自动换行


        self.TextShow1.setText(self.data[2])
        self.TextShow1.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 14))
        self.TextShow1.setStyleSheet("color: %s;"
                                     "border: 0px solid rgba(0,0,0,0)" % temp_qss.font_color2)
        self.TextShow1.setWordWrap(True)  # 自动换行

    def UIsite(self):
        # 如果有图片
        ans = [0]
        def f1():
            ans[0] = IsGoodImg(self.data[1])

        if IsGoodImg(self.data[1]):
            self.Textlayout.addWidget(self.NameLable)
            self.Textlayout.addWidget(self.TextShow1)
            self.TextBox.setLayout(self.Textlayout)
            self.layout.addWidget(self.ImgShow)
            # 把图片放进去
            self.ImgShow.setPixmap(GetImg(self.data[1]))
            self.layout.addWidget(self.TextBox)
            self.setLayout(self.layout)
            self.ImgShow.setMinimumSize(AllQss.img_max_w, AllQss.img_max_w)
            self.ImgShow.setMaximumSize(AllQss.img_max_w, AllQss.img_max_w)
        else:
            self.Textlayout.addWidget(self.NameLable)
            self.Textlayout.addWidget(self.TextShow1)
            self.TextBox.setLayout(self.Textlayout)
            self.layout.addWidget(self.TextBox)
            self.setLayout(self.layout)

    # 监听鼠标悬浮事件
    def enterEvent(self, event):
        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.dad.Theme) == "Day" else NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;''' % (temp_qss.select_fill_color))
        # 更新页码
        self.dad.SetPage(self.id)
        event.accept()

    # 监听鼠标离开事件
    def leaveEvent(self, event):
        # 获取主题色
        temp_qss = DayQss if GetTheme(self.dad.dad.Theme) == "Day" else NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;''' % (temp_qss.fill_color1))
        event.accept()

    # 监听鼠标点击事件
    def mousePressEvent(self, event):
        # 如果当前在根目录，也放弃操作
        if self.dad.dad.now_class.name == AllQss.text1:
            AlertWindow(self, "🥱", "<您当前在根目录>\n\n想要查看主题请点击左侧主题名称").show()
            return

        # 如果当前有其他窗口则放弃操作
        if self.DisPlayWindow != None:
            self.DisPlayWindow.activateWindow()
            return

        self.DisPlayWindow = self.newDisplay
        self.dad.DispalyIndoWindowList.append(self.newDisplay)   # 在列表里面加入这个窗口
        self.newDisplay.show()

    def SetDay(self):
        self.Theme = "Day"
        # 背景
        self.setStyleSheet('''background-color: %s;
                                      border-radius: 7px;''' % (DayQss.fill_color1))
        # 文字
        self.NameLable.setStyleSheet("font-weight: bold;color: %s;border: 0px" % DayQss.font_color1)
        self.TextShow1.setStyleSheet("color: %s;border: 0px" % DayQss.font_color2)

    def SetNight(self):
        self.Theme = "Night"
        # 背景
        self.setStyleSheet('''background-color: %s;
                                      border-radius: 7px;''' % (NightQss.fill_color1))
        # 文字
        self.NameLable.setStyleSheet("font-weight: bold;color: %s;border: 0px" % NightQss.font_color1)
        self.TextShow1.setStyleSheet("color: %s;border: 0px" % NightQss.font_color2)

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()

# 横向布局框框
class ShowContainer(QLabel):
    def __init__(self, name, dad):
        super(ShowContainer, self).__init__(name, dad)
        self.SetUp()

    def UIinit(self):
        self.layout = QVBoxLayout()  # 创建一个垂直布局
        self.scroll = QScrollArea()  # 创建一个滚动区域
        self.container = QWidget()   # 创建一个容器widget用于放置按钮


    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if GetTheme(AllQss.default_mode) == "Day" else NightQss

        # 减小布局的侧边距
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 滚动区域
        self.scroll.setWidgetResizable(True)  # 设置滚动区域的大小自适应
        self.scroll.setStyleSheet("background-color: %s;  /* 设置滚动区域的背景颜色 */"
                                    "border: 1px solid %s;  /* 边框色 */" % (temp_qss.fill_color2, temp_qss.fill_color2))
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 关掉滚动条

        # 放置
        self.container.setLayout(self.layout)
        self.scroll.setWidget(self.container)

        # 将滚动区域放入窗口
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scroll)

        # 放置进窗口
        self.setLayout(self.mainLayout)

    def SetDay(self):
        self.scroll.setStyleSheet("background-color: %s;  /* 设置滚动区域的背景颜色 */"
                                  "border: 1px solid %s;  /* 边框色 */" % (DayQss.fill_color2, DayQss.fill_color2))
        # 遍历子控件
        for i in range(self.layout.count() - 1):
            self.layout.itemAt(i).widget().SetDay()

    def SetNight(self):
        self.scroll.setStyleSheet("background-color: %s;  /* 设置滚动区域的背景颜色 */"
                                  "border: 1px solid %s;  /* 边框色 */" % (NightQss.fill_color2, NightQss.fill_color2))

        # 遍历子控件
        for i in range(self.layout.count() - 1):
            self.layout.itemAt(i).widget().SetNight()

    def SetUp(self):
        self.UIinit()
        self.UIcss()

# 横向布局框框有滚动条的那一个
class ShowContainerBar(QLabel):
    def __init__(self, name, dad):
        super(ShowContainerBar, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.info = None
        self.NowAddNum = 0
        self.UpDataIng = False  # 一个记录当前是不是在更新的变量，防止bug的
        self.DispalyIndoWindowList = []  # 储存展示详细信息的窗口
        self.SetUp()

    def UIinit(self):
        self.layout = QVBoxLayout()  # 创建一个垂直布局
        self.scroll = QScrollArea()  # 创建一个滚动区域
        self.container = QWidget()  # 创建一个容器widget用于放置按钮
        self.mybar = QtWidgets.QScrollBar()  # 我的滚动条

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if self.dad.Theme == "Day" else NightQss

        # 减小布局的侧边距
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 滚动区域
        self.scroll.setWidgetResizable(True)  # 设置滚动区域的大小自适应
        self.scroll.setStyleSheet("background-color: %s;  /* 设置滚动区域的背景颜色 */"
                                  "border: 1px solid %s;  /* 边框色 */" % (temp_qss.fill_color2, temp_qss.fill_color2))
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 关掉滚动条

        # 给这个滚动条添加属性
        self.mybar.setStyleSheet("""
             QScrollBar:vertical {
                  border-width: 0px;
                  border: none;
                  background:rgba(0, 0, 0, 0);
                  width:10px;

              }
              QScrollBar::handle:vertical {
                  background:  %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 6px;
              }
              QScrollBar::handle:vertical:hover {
                  background: %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 4px;
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
              """ % (temp_qss.fill_color1, temp_qss.stroke_color1))
        self.scroll.setVerticalScrollBar(self.mybar)  # 把滚动条附上去

        # 放置
        self.container.setLayout(self.layout)
        self.scroll.setWidget(self.container)

        # 将滚动区域放入窗口
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scroll)

        # 放置进窗口
        self.setLayout(self.mainLayout)

    def UIfun(self):
        # 根据滚动条是否到底部来判断是否需要增加控件
        def scrollbar_value_changed():
            if self.mybar.value() and self.mybar.value() == self.mybar.maximum() and self.NowAddNum != len(self.info):
                self.mybar.setEnabled(False)
                # 逐个加入各个信息
                k = 2  # 依次加入的最大个数
                id = self.NowAddNum + 1
                for data in self.info[self.NowAddNum:self.NowAddNum + k]:
                    box_temp = ShowLine('', self, data)
                    box_temp = ShowLine('', self, data)
                    box_temp.id = id
                    id += 1
                    self.layout.addWidget(box_temp)
                    QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

                self.NowAddNum = min(len(self.info), self.NowAddNum + k)
                self.dad.now_class.PageText.setText(" %d / %d" % (self.NowAddNum, len(self.info)))  # 更新页码
                if self.NowAddNum == len(self.info):
                    self.layout.addWidget(EmptBox('', self))  # 加入一个空的控件
                self.mybar.setEnabled(True)

        self.mybar.valueChanged.connect(scrollbar_value_changed)

    def SetDay(self):
        self.Theme = self.dad.Theme
        self.scroll.setStyleSheet("background-color: %s;  /* 设置滚动区域的背景颜色 */"
                                  "border: 1px solid %s;  /* 边框色 */" % (DayQss.fill_color2, DayQss.fill_color2))

        # 2.给这个滚动条添加属性
        self.mybar.setStyleSheet("""
             QScrollBar:vertical {
                  border-width: 0px;
                  border: none;
                  background:rgba(0, 0, 0, 0);
                  width:10px;

              }
              QScrollBar::handle:vertical {
                  background:  %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 6px;
              }
              QScrollBar::handle:vertical:hover {
                  background: %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 4px;
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
              """ % (DayQss.fill_color1, DayQss.stroke_color1))

        # 遍历子控件
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().SetDay()

        # 遍历子窗口
        for Diswindow in self.DispalyIndoWindowList:
            Diswindow.SetDay()
            Diswindow.activateWindow()

    def SetNight(self):
        self.Theme = self.dad.Theme
        self.scroll.setStyleSheet("background-color: %s;  /* 设置滚动区域的背景颜色 */"
                                  "border: 1px solid %s;  /* 边框色 */" % (NightQss.fill_color2, NightQss.fill_color2))

        # 2.给这个滚动条添加属性
        self.mybar.setStyleSheet("""
             QScrollBar:vertical {
                  border-width: 0px;
                  border: none;
                  background:rgba(0, 0, 0, 0);
                  width:10px;

              }
              QScrollBar::handle:vertical {
                  background:  %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 6px;
              }
              QScrollBar::handle:vertical:hover {
                  background: %s;
                  min-height: 20px;
                  max-height: 20px;
                  border-radius: 2px;
                  margin:0px 0px 0px 4px;
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
              """ % (NightQss.fill_color1, NightQss.stroke_color1))

        # 遍历子控件
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().SetNight()

        # 遍历子窗口
        for Diswindow in self.DispalyIndoWindowList:
            Diswindow.SetNight()
            Diswindow.activateWindow()

    # 更新内容(从表名字)
    def UpdataContainer(self, table_name):
        # 如果当前在更行就放弃这次更新
        if self.UpDataIng:
            return
        self.UpDataIng = True

        # 清空布局内的控件
        # self.RemoveItem()
        RemoveLayoutItem(self.layout)
        info = SQLopt.GetTableInfo(self.dad.cur, table_name)[1:]
        NowAddNum = min(len(info), 10)  # 当前已经加入的子控件的个数
        self.info = info
        self.NowAddNum = NowAddNum
        # 逐个加入各个信息
        id = 1
        for data in info[:NowAddNum]:
            box_temp = ShowLine('', self, data)
            box_temp.id = id
            id += 1
            self.layout.addWidget(box_temp)
            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

        if NowAddNum == len(info):
            self.layout.addWidget(EmptBox('', self, text="--没有更多了--"))  # 加入一个空的控件
        # 更新页码
        self.dad.now_class.PageText.setText(" %d / %d" % (self.NowAddNum, len(self.info)))  # 更新页码
        self.UpDataIng = False

    # 直接给信息
    def UpdataContainerFromData(self, info):
        # 如果当前在更行就放弃这次更新
        if self.UpDataIng:
            return
        self.UpDataIng = True

        # 清空布局内的控件
        # self.RemoveItem()
        RemoveLayoutItem(self.layout)
        NowAddNum = min(len(info), 10)  # 当前已经加入的子控件的个数
        self.info = info
        self.NowAddNum = NowAddNum
        # 逐个加入各个信息
        id = 1
        for data in info[:NowAddNum]:
            box_temp = ShowLine('', self, data)
            box_temp.id = id
            id += 1
            self.layout.addWidget(box_temp)
            QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

        if NowAddNum == len(info):
            self.layout.addWidget(EmptBox('', self, text="--没有更多了--"))  # 加入一个空的控件
        # 更新页码
        self.dad.now_class.PageText.setText(" %d / %d" % (self.NowAddNum, len(self.info)))  # 更新页码
        self.UpDataIng = False

    def RemoveItem(self):
        # 如果当前在更行就放弃这次更新
        if self.UpDataIng:
            return
        self.UpDataIng = True
        RemoveLayoutItem(self.layout)
        self.UpDataIng = False
        # self.DispalyIndoWindowList = []  # 储存展示详细信息的窗口

    def SetPage(self, num):
        # 更新页码
        self.dad.now_class.PageText.setText(" %d / %d" % (num, len(self.info)))  # 更新页码

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIfun()

# 左侧类别整体控件
class LeftLayout(QLabel):
    def __init__(self, name, dad):
        super(LeftLayout, self).__init__(name, dad)
        self.SetUp()

    def UIinit(self):
        self.layout = QVBoxLayout()  # 横向布局
        self.setLayout(self.layout)

    def SetUp(self):
        self.UIinit()

# 交互输入控制控件
class ChangeBox(QLabel):
    def __init__(self):
        super(ChangeBox, self).__init__()
        self.Name        = None  # 默认名字
        self.OptionaList = None  # 判定函数
        self.HelpTxt     = None  # 帮助文档
        self.SetUp()

    def UIinit(self):
        self.layout = QHBoxLayout()  # 横向布局
        self.NameLable = QLabel()    # 项目名称
        self.Input  = QComboBox()    # 输入
        self.Light  = QLabel()       # 输入提示框

    def UIcss(self):
        # 把各个控件加入布局
        self.layout.addWidget(self.NameLable)
        self.layout.addWidget(self.Input)
        self.layout.addWidget(self.Light)

        # 把布局加入控件
        self.setLayout(self.layout)

        # 背景
        self.setStyleSheet('''background-color: rgb(240, 240, 240);
                              border-radius: 3px;
                              border: 1px solid #c5c5c5; /* 边框色 */''')

        # 名字
        self.NameLable.setFont(QtGui.QFont("arial", AllQss.font_size + 10))
        self.NameLable.setMinimumSize(90, 30)  # 设置最小尺寸
        self.NameLable.setMaximumSize(90, 30)  # 设置最小尺寸
        self.NameLable.setStyleSheet('''background-color: rgb(240, 240, 240, 0);
                              border: 1px solid rgb(240, 240, 0, 0); /* 边框色 */''')


        # 输入框
        self.Input.setFont(QtGui.QFont("arial", AllQss.font_size + 10))
        self.Input.setMinimumSize(30, 30)  # 设置最小尺寸
        self.setStyleSheet('''background-color: rgb(240, 240, 240);
                              color: #000000;
                              border-radius: 3px;
                              border: 1px solid #c5c5c5; /* 边框色 */''')

        # 指示灯
        self.Light.setText("✔")
        self.Light.setFont(QtGui.QFont("arial", AllQss.font_size + 10))
        self.Light.setAlignment(Qt.AlignCenter)  # 将文本居中显示
        self.Light.setMinimumSize(20, 20)  # 设置最小尺寸
        self.Light.setMaximumSize(20, 20)  # 设置最大尺寸
        self.Light.setStyleSheet('''background-color: #0aea00;
                                    color: #ffffff;
                                      border-radius: 10px;
                                      border: 1px solid #7aea79; /* 边框色 */''')

    # 判断值是否合理
    def IsGoodVal(self):
        return True

    # 设置默认值
    def SetDefValue(self, val):
        self.Input.setCurrentText(val)

    # 设置可选列表
    def SetOptionaList(self, Set):
        self.OptionaList = Set
        for t in self.OptionaList:
            self.Input.addItem(t)

    # 更改label名称
    def SetLabelName(self, name):
        self.Name = name
        self.NameLable.setText(name)

    # 更改help文字
    def SetHelpTxt(self, txt):
        self.HelpTxt = txt
        QToolTip.setFont(QFont('SansSerif', 10))
        # setToolTip用于显示气泡提示
        self.Light.setToolTip(self.HelpTxt)

    # 获取当前信息
    def GetVal(self):
        return self.Input.currentText()

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()