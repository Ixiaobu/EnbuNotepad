from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QScrollArea, QWidget, QTextEdit, QMenu, QAction, QHBoxLayout
from AlertWindow import AlertWindow
from ZEBqt import EnbuBasicWindow
from ReadIni import AllQss, DayQss, NightQss
from EnbuQt import MoveButton, ShowClassName, EmptBox
from ToolFun import GetTheme, GetTime
from Check import CheckCreateTable
import SQLopt


# 横向布局框框有滚动条的那一个
class ShowContainerBar(QLabel):
    def __init__(self, name, dad):
        super(ShowContainerBar, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.info = None
        self.SetUp()

    def UIinit(self):
        self.layout = QVBoxLayout()  # 创建一个垂直布局
        self.scroll = QScrollArea()  # 创建一个滚动区域
        self.container = QWidget()  # 创建一个容器widget用于放置按钮
        self.mybar = QtWidgets.QScrollBar()  # 我的滚动条

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if self.Theme == "Day" else NightQss

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
        pass

    def SetDay(self):
        self.Theme = "Day"
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
        for i in range(11, self.layout.count() - 1):
            self.layout.itemAt(i).widget().SetDay()

    def SetNight(self):
        self.Theme = "Night"
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
        for i in range(11, self.layout.count() - 1):
            self.layout.itemAt(i).widget().SetNight()

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIfun()

# 自动改变大小的文本编辑框
class AutoResizeTextEdit(QTextEdit):
    def __init__(self, name, dad):
        super(AutoResizeTextEdit, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.DefaultText = ""  # 储存默认的文本
        self.setAcceptRichText(False)  # 设置QTextEdit只接受普通文本
        self.ResizeIng = False
        self.AutoResize()

    def resize(self):
        if self.ResizeIng:
            return
        self.ResizeIng = True
        try:
            vertical_scrollbar = self.verticalScrollBar()
            while not vertical_scrollbar.isVisible() and self.height() > 50:
                self.setMinimumHeight(self.height() - 1)
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
            while vertical_scrollbar.isVisible():
                self.setMinimumHeight(self.height() + 1)
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
        except:
            pass
        self.ResizeIng = False

    def AutoResize(self):
        temp_qss = DayQss if self.Theme == "Day" else NightQss
        self.setMinimumHeight(50)

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

        self.textChanged.connect(self.resize)

    # 设置默认文本的内容
    def SetDefaultText(self, text):
        self.DefaultText = text
        self.setText(self.DefaultText)

    def focusInEvent(self, event):
        if self.toPlainText() == self.DefaultText:
            self.clear()
        super(AutoResizeTextEdit, self).focusInEvent(event)

    def focusOutEvent(self, event):
        if not self.toPlainText():
            self.setPlainText(self.DefaultText)
        super(AutoResizeTextEdit, self).focusOutEvent(event)

# 自动改变大小的文本编辑框
class AutoResizeTextEditCanDel(QTextEdit):
    def __init__(self, name, dad):
        super(AutoResizeTextEditCanDel, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.setContextMenuPolicy(3)  # 设置右击菜单策略为CustomContextMenu
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.setAcceptRichText(False)  # 设置QTextEdit只接受普通文本
        self.AutoResize()

    def AutoResize(self):
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        self.setMinimumHeight(50)

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
        self.textChanged.connect(self.resize)

    def resize(self):
        try:
            vertical_scrollbar = self.verticalScrollBar()

            while not vertical_scrollbar.isVisible() and self.height() > 50:
                self.setMinimumHeight(self.height() - 1)
                self.dad.setMinimumHeight(self.dad.height() - 1)
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

            while vertical_scrollbar.isVisible():
                self.setMinimumHeight(self.height() + 1)
                self.dad.setMinimumHeight(self.dad.height() + 1)
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面
        except:
            pass

    def showContextMenu(self, pos):
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        # 右键菜单
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: %s; color: %s; border: 1px solid %s;border-radius: 5px; padding: 5px}"
                           "QMenu::item:selected { background-color: %s; color: %s; border: 1px solid %s;border-radius: 5px; padding: 5px}"
                           % (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.stroke_color1,
                              temp_qss.select_fill_color, temp_qss.font_color1, temp_qss.stroke_color1))  # 设置弹窗的样式表
        menu.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 12))  # 设置弹窗的字体

        action1 = QAction(QIcon(r"data\ico\ico5.png"), "删除该项", self)
        menu.addAction(action1)

        action = menu.exec_(self.mapToGlobal(pos))
        if action == action1:
            # 从布局中移除要删除的控件
            self.dad.dad.dad.Container.layout.removeWidget(self.dad)
            # 删除控件
            self.dad.deleteLater()

# 有上下箭头，删除按钮的控件
class UseSortTextEdit(QLabel):
    def __init__(self, name, dad):
        super(UseSortTextEdit, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme  # 储存深浅色
        self.SetUp()

    def UIinit(self):
        self.layout = QHBoxLayout()  # 横向布局
        self.Input  = AutoResizeTextEditCanDel('', self) # 文本输入

        self.ButtonBox    = QLabel('', self)  # 放按钮的容器
        self.ButtonLayout = QVBoxLayout()  # 放按钮的布局
        self.UpButton     = QPushButton('', self)  # 向上走
        self.DownButton   = QPushButton('', self)  # 向下走

    def UIcss(self):
        # 根据深浅色选择一个配置
        self.setMinimumHeight(50)
        temp_qss = DayQss if GetTheme(self.Theme) == "Day" else NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;
                              border: 0px''' % (temp_qss.fill_color1))

        # 输入
        self.Input.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Input.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 上
        self.UpButton.setFont(QtGui.QFont("arial", AllQss.font_size + 10))
        self.UpButton.setText(QtCore.QCoreApplication.translate("MainWindow", "▲"))
        self.UpButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

        # 下
        self.DownButton.setFont(QtGui.QFont("arial", AllQss.font_size + 10))
        self.DownButton.setText(QtCore.QCoreApplication.translate("MainWindow", "▼"))
        self.DownButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

        self.ButtonBox.setMinimumWidth(50)  # 按钮的最小尺寸
        self.layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0
        self.ButtonLayout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0

    def UIsite(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.Input)
        self.layout.addWidget(self.ButtonBox)

        self.ButtonLayout.addWidget(self.UpButton)
        self.ButtonLayout.addWidget(self.DownButton)
        self.ButtonBox.setLayout(self.ButtonLayout)

    def UIfun(self):
        # 上移
        def Up():
            temp_layout = self.dad.dad.Container.layout
            index = temp_layout.indexOf(self)
            if index > 11:
                temp_layout.insertWidget(index - 1, self)

        self.UpButton.clicked.connect(Up)

        # 下移
        def Down():
            temp_layout = self.dad.dad.Container.layout
            index = temp_layout.indexOf(self)
            if index < temp_layout.count() - 3:
                temp_layout.insertWidget(index + 1, self)
        self.DownButton.clicked.connect(Down)

    def toPlainText(self):
        return self.Input.toPlainText()

    def SetDay(self):
        self.Theme = "Day"
        temp_qss = DayQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;
                              border: 0px''' % (temp_qss.fill_color1))

        # 输入
        self.Input.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))
        # 上
        self.UpButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

        # 下
        self.DownButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

    def SetNight(self):
        self.Theme = "Night"
        temp_qss = NightQss
        # 背景
        self.setStyleSheet('''background-color: %s;
                              border-radius: 7px;
                              border: 0px''' % (temp_qss.fill_color1))

        # 输入
        self.Input.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))
        # 上
        self.UpButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

        # 下
        self.DownButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s}''' %
            (temp_qss.font_color1, temp_qss.theme_color))

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

# 添加表头
class AddTableName(QPushButton):
    def __init__(self, name, dad):
        super(AddTableName, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.SetUp()

    def UIcss(self):
        # 获取主题色
        temp_qss = DayQss if self.dad.Theme == "Day" else NightQss

        self.setFont(QtGui.QFont("arial", AllQss.font_size + 40))
        self.setText(QtCore.QCoreApplication.translate("MainWindow", "+"))
        self.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 0px;color: %s;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.select_fill_color, temp_qss.font_color1))

    def UIfun(self):
        def fun():
            # 获取主题色
            temp_qss = DayQss if self.dad.Theme == "Day" else NightQss
            temp = UseSortTextEdit('', self)
            self.dad.Container.layout.insertWidget(self.dad.Container.layout.count() - 2, temp)
            temp.Input.resize()
        self.clicked.connect(fun)

    def SetDay(self):
        self.Theme = "Day"
        self.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 0px;color: %s;}''' %
            (DayQss.fill_color1, DayQss.font_color1, DayQss.select_fill_color, DayQss.font_color1))

    def SetNight(self):
        self.Theme = "Night"
        self.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 7px;border: 0px;color: %s;}
            QPushButton:hover{background:%s;border-radius: 7px;border: 0px;color: %s;}''' %
            (NightQss.fill_color1, NightQss.font_color1, NightQss.select_fill_color, NightQss.font_color1))

    def SetUp(self):
        self.UIcss()
        self.UIfun()

# 选择列表
class ChoiceBox(QLabel):
    def __init__(self, name, dad):
        super(ChoiceBox, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.site = 0  # 下标
        self.mod  = ["文本内容", "图片内容"]  # 主题标记
        self.SetUp()

    def UIinit(self):
        self.layout = QHBoxLayout()  # 布局
        self.ShowLable = QLabel('', self)  # 显示当前选项
        self.Button    = QPushButton('', self)  # 更改格式的按钮

    def UIcss(self):
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        # 背景
        self.setStyleSheet('''background-color: %s ;
                            border-radius: 7px''' % (temp_qss.fill_color1))
        self.setMinimumHeight(50)


        # 文本框
        self.ShowLable.setText(self.mod[0])
        self.ShowLable.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.ShowLable.setStyleSheet('''color:%s;border: 0px}''' % (temp_qss.font_color1))

        # 按钮
        self.Button.setText(">")
        self.Button.setFont(QtGui.QFont("arial", AllQss.font_size + 18))
        self.Button.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s;border: 0px}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s;border: 0px}''' %
            (temp_qss.font_color2, temp_qss.theme_color))
        self.Button.setMaximumWidth(50)

        # 放置
        self.setLayout(self.layout)
        self.layout.addWidget(self.ShowLable)
        self.layout.addWidget(self.Button)

    def UIfun(self):
        def Change():
            self.site = (self.site + 1) % len(self.mod)
            self.ShowLable.setText(self.mod[self.site])
        self.Button.clicked.connect(Change)

    def GetText(self):
        return self.mod[self.site]

    def SetDay(self):
        temp_qss = DayQss
        self.Theme = "Day"

        # 背景
        self.setStyleSheet('''background-color: %s ;
                                    border-radius: 7px''' % (temp_qss.fill_color1))

        # 文本框
        self.ShowLable.setStyleSheet('''color:%s;; border: 0px}''' % (temp_qss.font_color1))

        # 按钮
        self.Button.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s;border: 0px}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s;border: 0px}''' %
            (temp_qss.font_color2, temp_qss.theme_color))

    def SetNight(self):
        temp_qss = NightQss
        self.Theme = "Night"

        # 背景
        self.setStyleSheet('''background-color: %s ;
                                    border-radius: 7px''' % (temp_qss.fill_color1))

        # 文本框
        self.ShowLable.setStyleSheet('''color:%s; border: 0px}''' % (temp_qss.font_color1))

        # 按钮
        self.Button.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s;border: 0px}
            QPushButton:hover{background:rgb(0,0,0,0);color:%s;border: 0px}''' %
            (temp_qss.font_color2, temp_qss.theme_color))

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIfun()

# 主窗口类
class AddClassWindow(EnbuBasicWindow):
    def __init__(self, dad):
        super(AddClassWindow, self).__init__()
        self.dad = dad
        self.Theme = self.dad.Theme  # 储存深浅色
        self.resize(450, 500)  # 尺寸
        self.SetUp()

    def UIinit(self):
        self.BackGround  = QLabel('', self)         # 背景
        self.MiniButton  = QPushButton('', self)    # 最小化按钮
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.ResizeBtn   = MoveButton('', self)     # 缩放按钮

        self.Container = ShowContainerBar('', self)  # 一个容器
        self.ClassName = AutoResizeTextEdit('', self)  # 名字
        self.ClassRemarks = AutoResizeTextEdit('', self)  # 描述
        self.ClassTypes   = ChoiceBox('', self)  # 主题类型
        self.ClassPassWord = AutoResizeTextEdit('', self)  # 密码
        self.AddNameButton = AddTableName('', self)  # 添加名字
        self.Name1 = AutoResizeTextEdit('', self)  # 主题
        self.Name2 = AutoResizeTextEdit('', self)  # 图片
        self.FinishButton = QPushButton('', self)  # 完成按钮

        self.text1 = QLabel('', self)
        self.text2 = QLabel('', self)
        self.text3 = QLabel('', self)
        self.text4 = QLabel('', self)
        self.text5 = QLabel('', self)

    def UIcss(self, first=True):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if GetTheme(self.Theme) == "Day" else NightQss

        # 背景
        self.BackGround.setStyleSheet('''background-color: %s ;
                                        border: 1px solid %s;
                                        border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))
        if first:
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

        # 名字
        self.ClassName.SetDefaultText("在这里键入名称")
        self.ClassName.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.ClassName.setStyleSheet('''QTextEdit {background-color: %s;
                                          border-radius: 7px;
                                          border: 0px;
                                          color:%s;
                                          padding: 10px;}
                                          ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 密码
        self.ClassPassWord.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.ClassPassWord.setStyleSheet('''QTextEdit {background-color: %s;
                                          border-radius: 7px;
                                          border: 0px;
                                          color:%s;
                                          padding: 10px;}
                                          ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 描述
        self.ClassRemarks.SetDefaultText("在这里键入描述")
        self.ClassRemarks.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.ClassRemarks.setStyleSheet('''QTextEdit {background-color: %s;
                                          border-radius: 7px;
                                          border: 0px;
                                          color:%s;
                                          padding: 10px;}
                                          ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.Name1.setText("标题")
        self.Name1.setReadOnly(True)  # 设置QTextEdit为只读
        self.Name1.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Name1.setStyleSheet('''QTextEdit {background-color: %s;
                                          border-radius: 7px;
                                          border: 0px;
                                          color:%s;
                                          padding: 10px;
                                          font-weight: bold;}
                                          ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.Name2.setText("图片")
        self.Name2.setReadOnly(True)  # 设置QTextEdit为只读
        self.Name2.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 16))
        self.Name2.setStyleSheet('''QTextEdit {background-color: %s;
                                          border-radius: 7px;
                                          border: 0px;
                                          color:%s;
                                          padding: 10px;
                                          font-weight: bold;}
                                          ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.FinishButton.setText(QtCore.QCoreApplication.translate("MainWindow", "ok"))
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.FinishButton.setGraphicsEffect(self.Get_Shaow())

        self.text1.setText("添加新的主题")
        self.text1.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 22))
        self.text1.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.theme_color))

        self.text2.setText("基本信息")
        self.text2.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 14))
        self.text2.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))

        self.text3.setText("主题类型")
        self.text3.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 14))
        self.text3.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))

        self.text4.setText("设置密码")
        self.text4.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 14))
        self.text4.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))

        self.text5.setText("标签列表")
        self.text5.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 14))
        self.text5.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))

    def UIsite(self):
        # 背景
        k = 25  # 边距变量
        self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))

        # 最小化按钮
        self.MiniButton.setGeometry(QtCore.QRect(self.width() - 75 - k, k - 7, 30, 30))

        # 关闭
        self.CloseButton.setGeometry(QtCore.QRect(self.width() - 45 - k, k - 5, 30, 30))

        # 缩放按钮
        self.ResizeBtn.setGeometry(QtCore.QRect(self.width() - k - 35, self.height() - k - 35, 30, 30))

        # 容器
        self.Container.setGeometry(QtCore.QRect(k + 5, k + 20, self.width() - 2 * k - 20, self.height() - 2 * k - 50))

        # 完成按钮
        self.FinishButton.setGeometry(QtCore.QRect(self.width() - 100 - 25, self.height() - 110 - 25, 60, 60))

        # 放置
        self.Container.layout.addWidget(self.text1)
        self.Container.layout.addWidget(self.text2)
        self.Container.layout.addWidget(self.ClassName)
        self.Container.layout.addWidget(self.ClassRemarks)
        self.Container.layout.addWidget(self.text3)
        self.Container.layout.addWidget(self.ClassTypes)
        self.Container.layout.addWidget(self.text4)
        self.Container.layout.addWidget(self.ClassPassWord)
        self.Container.layout.addWidget(self.text5)
        self.Container.layout.addWidget(self.Name1)
        self.Container.layout.addWidget(self.Name2)
        self.Container.layout.addWidget(self.AddNameButton)
        self.Container.layout.addWidget(EmptBox('', self))  # 加入一个空的

    def UIfun(self):
        # 关闭按钮
        def ClossAll():
            self.dad.ChildWindow = None
            self.close()
        self.CloseButton.clicked.connect(ClossAll)

        # 最小按钮
        self.MiniButton.clicked.connect(lambda x: self.showMinimized())

        # 缩放界面
        def ResizeWindow():
            k = 25
            w, h = self.ResizeBtn.x() + k + 35, self.ResizeBtn.y() + k + 35
            self.resize(w, h) # 总窗口尺寸

            self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))
            self.MiniButton.setGeometry(QtCore.QRect(self.width() - 75 - k, k - 7, 30, 30))  # 最小化按钮
            self.CloseButton.setGeometry(QtCore.QRect(self.width() - 45 - k, k - 5, 30, 30))  # 关闭
            self.Container.setGeometry(QtCore.QRect(k + 5, k + 20, self.width() - 2 * k - 20, self.height() - 2 * k - 50))  # 容器
            self.FinishButton.setGeometry(QtCore.QRect(self.width() - 100 - 25, self.height() - 110 - 25, 60, 60))  # 完成按钮

        self.ResizeBtn.siteChanged.connect(ResizeWindow)

        # 完成
        def Finish():
            name = self.Container.layout.itemAt(2).widget().toPlainText()  # 名字
            creak_time = GetTime()  # 创建时间
            remark = self.Container.layout.itemAt(3).widget().toPlainText()  # 描述
            mod = self.Container.layout.itemAt(5).widget().GetText()  # 文本类型
            password = self.Container.layout.itemAt(7).widget().toPlainText()  # 密码
            data1 = [name, creak_time, remark, mod, password, ""]

            # 导入表头
            data2 = []
            for i in range(9, self.Container.layout.count() - 2):
                data2.append(self.Container.layout.itemAt(i).widget().toPlainText())
            data2.append("备注")
            data2.append("创建时间")

            # 检查输入
            if not CheckCreateTable(self, self.dad.cur, data1, data2):
                return

            # 在数据库内创建
            if not SQLopt.CreateTable(self.dad.conn, self.dad.cur, data1, data2):
                AlertWindow(self, "🤯", "未知的严重错误，请检查您的输入是否包含了特殊字符，或使用数字作为开头").show()
                return

            # 更新左边的名字
            box_temp = ShowClassName('', self.dad, data1)
            self.dad.ShowClass.layout.insertWidget(self.dad.ShowClass.layout.count() - 2, box_temp)  # 插入
            box_temp.Clicked()  # 直接调到新建的窗口
            self.dad.Container.UpdataContainer(box_temp.name if box_temp.name != AllQss.text1 else "根目录")  # 更新主窗口的内容

            ClossAll() # 运行完就关掉

        self.FinishButton.clicked.connect(Finish)

    def SetDay(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss
        self.Theme = "Day"

        # 背景
        self.BackGround.setStyleSheet('''background-color: %s ;
                                                border: 1px solid %s;
                                                border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))

        # 最小化按钮
        self.MiniButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

        # 缩放
        self.ResizeBtn.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color2))

        # 名字
        self.ClassName.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 密码
        self.ClassPassWord.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 描述
        self.ClassRemarks.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.Name1.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.Name2.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))

        self.text1.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.theme_color))
        self.text2.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))
        self.text3.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))
        self.text4.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))
        self.text5.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))

        # 容器
        self.Container.SetDay()
        # 选择
        self.ClassTypes.SetDay()

    def SetNight(self):
        # 根据深浅色选择一个配置
        temp_qss = NightQss
        self.Theme = "Night"

        # 背景
        self.BackGround.setStyleSheet('''background-color: %s ;
                                                border: 1px solid %s;
                                                border-radius: 7px''' % (temp_qss.fill_color2, temp_qss.stroke_color1))

        # 最小化按钮
        self.MiniButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

        self.CloseButton.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color1))

        # 缩放
        self.ResizeBtn.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);color:%s}
            QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''' %
            (temp_qss.font_color2))

        # 名字
        self.ClassName.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 密码
        self.ClassPassWord.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 描述
        self.ClassRemarks.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.Name1.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.Name2.setStyleSheet('''QTextEdit {background-color: %s;
                                                  border-radius: 7px;
                                                  border: 0px;
                                                  color:%s;
                                                  padding: 10px;
                                                  font-weight: bold;}
                                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))

        self.text1.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.theme_color))
        self.text2.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))
        self.text3.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))
        self.text4.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))
        self.text5.setStyleSheet('''color:%s;font-weight: bold;}''' % (temp_qss.font_color1))

        # 容器
        self.Container.SetNight()
        # 选择
        self.ClassTypes.SetNight()

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AddClassWindow()  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程