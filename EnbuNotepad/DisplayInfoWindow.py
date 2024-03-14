from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QTextEdit, QHBoxLayout, QLineEdit

import SQLopt
from AlertWindow import AlertWindow
from Check import CheckAddInfo
from QuestionWindow import QuestionWindow
from ReadIni import AllQss, DayQss, NightQss
from ToolFun import GetTheme, GetImg, GetAllTime, ShowDifferent, IsGoodImg
from ZEBqt import EnbuBasicWindow


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
        self.text1.setStyleSheet("font-weight: bold;color: %s" % DayQss.theme_color)
        self.text2.setStyleSheet("color: %s" % DayQss.font_color1)
        self.text3.setStyleSheet("color: %s" % DayQss.font_color1)

    def SetNight(self):
        self.text1.setStyleSheet("font-weight: bold;color: %s" % NightQss.theme_color)
        self.text2.setStyleSheet("color: %s" % NightQss.font_color1)
        self.text3.setStyleSheet("color: %s" % NightQss.font_color1)

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()

# 横向布局框框有滚动条的那一个
class ShowContainerBar(QLabel):
    def __init__(self, name, dad):
        super(ShowContainerBar, self).__init__(name, dad)
        self.Theme = dad.Theme  # 储存深浅色
        self.dad = dad
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
        for i in range(self.layout.count() - 2):
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
        for i in range(self.layout.count() - 2):
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
        self.setAcceptRichText(False)  # 设置QTextEdit只接受普通文本
        self.ResizeIng = False
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


        def resize():
            if self.ResizeIng:
                return
            self.ResizeIng = True
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
            self.ResizeIng = False
        self.textChanged.connect(resize)

# 图片拖入显示
class ImgInputAndShow(QLabel):
    def __init__(self, name, dad):
        super(ImgInputAndShow, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.imgin = False
        self.default_img_path = {"Day":r".\data\img\day.png",
                                 "Night":r".\data\img\night.png"}
        self.path = ""
        self.SetUp()

    def UIinit(self):
        self.InputQt = QTextEdit('', self)  # 接收输入的内容

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        # 接收框
        self.InputQt.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                        border: 0px;
                                        color: rgba(0, 0, 0, 0)''')
        # 图片显示格式
        img = GetImg(self.default_img_path[self.Theme])
        self.setPixmap(img)
        self.setScaledContents(True)  # 图片大小自适应

    def UIsite(self):
        # 让输入和显示一样大，并且可以缩放
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.InputQt)
        self.setLayout(self.layout)

    def UIfun(self):
        def ChangeImg():
            # 如果是空的就退出去
            if self.InputQt.toPlainText() == "":
                return

            self.path = self.InputQt.toPlainText()[8:]
            try:
                img = GetImg(self.path)
                self.setPixmap(img)
                self.InputQt.setText("")
                self.imgin = True
            except:
                self.path = ""
                self.InputQt.setText("")
                img = GetImg(self.default_img_path[self.Theme])
                self.setPixmap(img)
                AlertWindow(self, "🤯", "你输入的图片似乎有点问题，请重新输入（将图片拖入加号处）").show()

        self.InputQt.textChanged.connect(ChangeImg)

    def SetImg(self, img):
        if img:
            img = GetImg(img)
            self.setPixmap(img)
            self.path = img
            self.imgin = True

    def SetDay(self):
        self.Theme = "Day"
        # 根据深浅色选择一个配置
        temp_qss = DayQss

        # 接收框
        self.InputQt.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                                border: 0px;
                                                color: rgba(0, 0, 0, 0)''')
        # 图片显示格式
        if not self.imgin:
            img = GetImg(r".\data\img\day.png")
            self.setPixmap(img)

    def SetNight(self):
        self.Theme = "Night"
        # 根据深浅色选择一个配置
        temp_qss = NightQss

        # 接收框
        self.InputQt.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                                border: 0px;
                                                color: rgba(0, 0, 0, 0)''')
        # 图片显示格式
        if not self.imgin:
            img = GetImg(r".\data\img\night.png")
            self.setPixmap(img)

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

# 左边是图片输入，右边是名称输入
class ImgAndNameInput(QLabel):
    def __init__(self, name, dad):
        super(ImgAndNameInput, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.SetUp()

    def UIinit(self):
        self.layout = QHBoxLayout()  # 横向布局
        self.ImgIn  = ImgInputAndShow('', self)  # 图片输入

        self.TextBoxName = QLabel('', self)  # 文本
        self.TextBoxNameLay = QVBoxLayout()  # 文本的布局
        self.NameTitle = QLabel('', self)  # 文本名字
        self.NameIn = QLineEdit('', self)  # 文本输入

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        self.setMinimumSize(120, 120)  # 设置输入的最小尺寸
        self.setMaximumSize(1000000, 200)  # 设置输入的最小尺寸

        # 图片输入
        self.ImgIn.setMinimumSize(100, 100)
        self.ImgIn.setMaximumSize(100, 100)

        # 输入
        self.NameTitle.setText("标题")
        self.NameTitle.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.NameTitle.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                    border: 0px;
                                    font-weight: bold;color: %s''' % (temp_qss.font_color1))

        # 输入
        self.NameIn.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 18))
        self.NameIn.setStyleSheet('''background-color: %s;
                                  border-radius: 7px;
                                  border: 0px;
                                  color:%s;
                                  padding: 10px;''' % (temp_qss.fill_color1, temp_qss.font_color1))

        self.TextBoxNameLay.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0

        self.setMaximumSize(10000, 120)

    def UIsite(self):
        self.layout.addWidget(self.ImgIn)  # 放置图片输入
        self.layout.addWidget(self.TextBoxName)  # 放置文本
        self.TextBoxName.setLayout(self.TextBoxNameLay)
        self.TextBoxNameLay.addWidget(self.NameTitle)
        self.TextBoxNameLay.addWidget(self.NameIn)
        self.setLayout(self.layout)  # 放置布局

    # 返回输入
    def GetText(self):
        return self.NameIn.text(), self.ImgIn.path

    def UIfun(self):
        pass

    def SetDay(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss
        self.Theme = "Day"

        # 图片输入
        self.ImgIn.SetDay()

        # 输入
        self.NameTitle.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                    border: 0px;
                                    font-weight: bold;color: %s''' % (temp_qss.font_color1))

        # 输入
        self.NameIn.setStyleSheet('''background-color: %s;
                                  border-radius: 7px;
                                  border: 0px;
                                  color:%s;
                                  padding: 10px;''' % (temp_qss.fill_color1, temp_qss.font_color1))

    def SetNight(self):
        # 根据深浅色选择一个配置
        temp_qss = NightQss
        self.Theme = "Night"

        # 图片输入
        self.ImgIn.SetNight()

        # 输入
        self.NameTitle.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                    border: 0px;
                                    font-weight: bold;color: %s''' % (temp_qss.font_color1))

        # 输入
        self.NameIn.setStyleSheet('''background-color: %s;
                                  border-radius: 7px;
                                  border: 0px;
                                  color:%s;
                                  padding: 10px;''' % (temp_qss.fill_color1, temp_qss.font_color1))

    # 填入图片和名字
    def SetData(self, name, img):
        if img:
            img = GetImg(img)
            self.ImgIn.setPixmap(img)
            self.ImgIn.imgin = True
        self.NameIn.setText(name)

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

# 图片显示，自动调整尺寸（保留原尺寸）
class ImgInputAndShowAutoResize(QLabel):
    def __init__(self, name, dad):
        super(ImgInputAndShowAutoResize, self).__init__(name, dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.path = ""
        self.img = None
        self.default_img_path = {"Day":r".\data\img\day.png",
                                 "Night":r".\data\img\night.png"}
        self.SetUp()

    def UIinit(self):
        self.InputQt = QTextEdit('', self)  # 接收输入的内容

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        # 接收框
        self.InputQt.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                        border: 0px;
                                        color: rgba(0, 0, 0, 0)''')
        # 图片显示格式
        self.img = GetImg(self.default_img_path[self.Theme], Square=False)
        self.setPixmap(self.img)
        self.setScaledContents(True)  # 图片大小自适应

    def UIsite(self):
        # 让输入和显示一样大，并且可以缩放
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.InputQt)
        self.setLayout(self.layout)

    def UIfun(self):
        def ChangeImg():
            # 如果是空的就退出去
            if self.InputQt.toPlainText() == "":
                return
            self.path = self.InputQt.toPlainText()[8:]
            try:
                self.img = GetImg(self.path, Square=False)
                self.setPixmap(self.img)
                self.InputQt.setText("")
                self.AutoResize()
                self.dad.ResizeWindow()
            except:
                self.path = ""
                self.InputQt.setText("")
                self.img = GetImg(self.default_img_path[self.Theme], Square=False)
                self.setPixmap(self.img)
                AlertWindow(self, "🤯", "你输入的图片似乎有点问题，请重新输入（将图片拖入加号处）").show()

        self.InputQt.textChanged.connect(ChangeImg)

    def SetDay(self):
        self.Theme = "Day"
        # 根据深浅色选择一个配置
        temp_qss = DayQss

        # 接收框
        self.InputQt.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                                border: 0px;
                                                color: rgba(0, 0, 0, 0)''')
        # 图片显示格式
        img = GetImg(r".\data\img\day.png")
        self.setPixmap(img)

    def SetNight(self):
        self.Theme = "Night"
        # 根据深浅色选择一个配置
        temp_qss = NightQss

        # 接收框
        self.InputQt.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                                border: 0px;
                                                color: rgba(0, 0, 0, 0)''')
        # 图片显示格式
        img = GetImg(r".\data\img\night.png")
        self.setPixmap(img)

    def SetImg(self, img):
        if IsGoodImg(img):
            self.path = img
            self.img = GetImg(img, Square=False)
            self.setPixmap(self.img)
            self.imgin = True
            self.AutoResize()
            self.dad.ResizeWindow()
        else:
            pass

    def AutoResize(self):
        width, height = self.img.width(), self.img.height()
        width_ = self.dad.width() - 100
        height_ = min(self.dad.height() - 100, int((width_ / width) * height))
        self.resize(width_, height_)
        QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

# 普通输入窗口
class TextInput(QLabel):
    def __init__(self, name, dad):
        super(TextInput, self).__init__("", dad)
        self.dad = dad
        self.Theme = self.dad.Theme
        self.name = name
        self.SetUp()

    def UIinit(self):
        self.layout = QVBoxLayout()  # 布局
        self.Title = QLabel('', self)  # 名字
        self.Input = AutoResizeTextEdit('', self)  # 输入

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

        self.setMinimumSize(100, 100)  # 设置输入的最小尺寸

        # 输入
        self.Title.setText(self.name)
        self.Title.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.Title.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                    border: 0px;
                                    font-weight: bold;color: %s''' % (temp_qss.font_color1))

        # 输入
        self.Input.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.Input.setStyleSheet('''QTextEdit {background-color: %s;
                                  border-radius: 7px;
                                  border: 0px;
                                  color:%s;
                                  padding: 10px;}
                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

    def UIsite(self):
        self.layout.addWidget(self.Title)
        self.layout.addWidget(self.Input)
        self.setLayout(self.layout)

    def GetText(self):
        return self.Input.toPlainText()

    def SetDay(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss
        self.Theme = "Day"

        self.setMinimumSize(100, 100)  # 设置输入的最小尺寸

        # 输入
        self.Title.setText(self.name)
        self.Title.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.Title.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                    border: 0px;
                                    font-weight: bold;color: %s''' % (temp_qss.font_color1))

        # 输入
        self.Input.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.Input.setStyleSheet('''QTextEdit {background-color: %s;
                                  border-radius: 7px;
                                  border: 0px;
                                  color:%s;
                                  padding: 10px;}
                                  ''' % (temp_qss.fill_color1, temp_qss.font_color1))

    def SetNight(self):
        # 根据深浅色选择一个配置
        temp_qss = NightQss
        self.Theme = "Night"

        self.setMinimumSize(100, 100)  # 设置输入的最小尺寸

        # 输入
        self.Title.setText(self.name)
        self.Title.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.Title.setStyleSheet('''background-color: rgba(0, 0, 0, 0);
                                            border: 0px;
                                            font-weight: bold;color: %s''' % (temp_qss.font_color1))

        # 输入
        self.Input.setFont(QtGui.QFont(AllQss.font, AllQss.font_size + 15))
        self.Input.setStyleSheet('''QTextEdit {background-color: %s;
                                          border-radius: 7px;
                                          border: 0px;
                                          color:%s;
                                          padding: 10px;}
                                          ''' % (temp_qss.fill_color1, temp_qss.font_color1))

    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()

def DisplayInfoWindow(name, dad, data):
    if dad.dad.dad.now_class.data[3] == "文本内容":
        return DisplayInfoWindowSamllImg(name, dad, data)
    else:
        return DisplayInfoWindowBigImg(name, dad, data)

# 展示、修改信息窗口(文字格式)
class DisplayInfoWindowSamllImg(EnbuBasicWindow):
    def __init__(self, name, dad, data):
        super(DisplayInfoWindowSamllImg, self).__init__()
        self.Theme = dad.Theme  # 储存深浅色
        self.dad = dad
        self.data = data
        self.ChildWindow = None  # 子窗口打开情况
        self.resize(450, 500)  # 尺寸

    def UIinit(self):
        self.Theme = self.dad.Theme
        self.BackGround  = QLabel('', self)         # 背景
        self.MiniButton  = QPushButton('', self)    # 最小化按钮
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.ResizeBtn   = MoveButton('', self)     # 缩放按钮
        self.Title       = QLabel('', self)         # 标题
        self.ImgAndNameInputQt = ImgAndNameInput('', self) # 图片和名字入

        self.Container       = ShowContainerBar('', self) # 一个容器
        self.TextBox         = TextBox('', self)  # 显示仓库信息文本

        self.DelButton    = QPushButton('', self)  # 删除按钮
        self.FinishButton = QPushButton('', self)  # 保存按钮

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

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

        # 更改文本
        self.TextBox.text1.setText(self.dad.dad.dad.now_class.name)
        self.TextBox.text2.setText(self.dad.dad.dad.now_class.create_time)
        self.TextBox.text3.setText(self.dad.dad.dad.now_class.remarks)

        self.DelButton.setText("")
        self.DelButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.DelButton.setStyleSheet(
            '''QPushButton{background:%s;color:%s;border-radius: 7px;}
            QPushButton:hover{background:rgb(244,71,53);color:%s;border-radius: 7px;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.font_color1))
        self.DelButton.setMinimumWidth(140)

        # 完成按钮
        self.FinishButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.FinishButton.setText(QtCore.QCoreApplication.translate("MainWindow", "ok"))
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.FinishButton.setGraphicsEffect(self.Get_Shaow())

        # 放图片，名字
        self.ImgAndNameInputQt.SetData(self.data[0], self.data[1])

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

        # 标题
        self.Title.setGeometry(QtCore.QRect(k + 7, k + 5, 100, 20))

        # 容器
        self.Container.setGeometry(QtCore.QRect(k + 5, k + 20, self.width() - 2 * k - 20, self.height() - 2 * k - 50))

        # 放置控件
        self.Container.layout.addWidget(self.TextBox)  # 加入文本
        self.Container.layout.addWidget(self.ImgAndNameInputQt)  # 加入图片名字
        i = 2
        for name in SQLopt.GetTableName(self.dad.dad.dad.cur, self.dad.dad.dad.now_class.name)[2:-1]:
            temp = TextInput(name, self)
            temp.Input.setText(self.data[i])
            i += 1
            self.Container.layout.addWidget(temp)

        self.Container.layout.addWidget(self.DelButton, 1, Qt.AlignHCenter)  # 删除按钮
        self.Container.layout.addWidget(EmptBox('', self))  # 加入一个空的

        # 完成按钮
        self.FinishButton.setGeometry(QtCore.QRect(self.width() - 100 - 25, self.height() - 110 - 25, 60, 60))

    def UIfun(self):
        # 关闭按钮
        def ClossAll():
            self.dad.dad.DispalyIndoWindowList.remove(self.dad.DisPlayWindow)
            self.dad.DisPlayWindow = None
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

        # 编辑完成
        def InputFinish():
            data = list(self.Container.layout.itemAt(1).widget().GetText())
            # 遍历子控件
            for i in range(2, self.Container.layout.count() - 2):
                data.append(self.Container.layout.itemAt(i).widget().GetText())

            # 检查输入是否合格
            if not CheckAddInfo(self, data):
                return

            # 检查输入是否有改变
            different_text = ShowDifferent(SQLopt.GetTableName(self.dad.dad.dad.cur,
                                                 self.dad.dad.dad.now_class.name),
                             self.data,
                             data)
            if different_text:
                def fun_true():
                    # 添加进数据库
                    data.append(GetAllTime())
                    SQLopt.ReplaceRow(self.dad.dad.dad.conn,
                                      self.dad.dad.dad.cur,
                                      self.dad.dad.dad.now_class.name,
                                      SQLopt.GetTableName(self.dad.dad.dad.cur,
                                                          self.dad.dad.dad.now_class.name),
                                      self.data,
                                      data)

                    ClossAll()
                    self.dad.dad.dad.Container.UpdataContainer(self.dad.dad.dad.now_class.name)  # 更新右边的容器

                    # 弹出提示
                    AlertWindow(self, "🥳", "<%s>更新成功！" % (data[0])).show()

                QuestionWindow(self, "🧐", "您确定更新吗\n\n" + different_text, lambda :None, fun_true).show()

            else:
                ClossAll()



        self.FinishButton.clicked.connect(InputFinish)

        # 删除信息
        def DelInfo():
            def fun_true():
                # 从数据库中删除
                SQLopt.DelereRow(self.dad.dad.dad.conn, self.dad.dad.dad.cur,
                                self.dad.dad.dad.now_class.name,
                                SQLopt.GetTableName(self.dad.dad.dad.cur, self.dad.dad.dad.now_class.name),
                                self.data)

                # 从布局中移除要删除的控件
                try:
                    self.dad.dad.dad.Container.layout.removeWidget(self.dad)
                    self.dad.setVisible(False)  # 隐藏控件
                except:
                    self.dad.dad.dad.Container.UpdataContainer(self.dad.dad.dad.now_class.name)

                ClossAll()  # 关闭控件
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

            QuestionWindow(self, "🥲", "<这个操作是不可逆转的>\n真的要删除 %s的 \n %s 吗？" % (self.dad.dad.dad.now_class.name, self.data[0]),
                           lambda: None, fun_true).show()

        self.DelButton.clicked.connect(DelInfo)

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

        # 文本
        self.TextBox.SetDay()

        # 容器
        self.Container.SetDay()

        # 删除按钮
        self.DelButton.setStyleSheet(
            '''QPushButton{background:%s;color:%s;border-radius: 7px;}
            QPushButton:hover{background:rgb(244,71,53);color:%s;border-radius: 7px;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))

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

        # 文本
        self.TextBox.SetNight()

        # 容器
        self.Container.SetNight()

        # 删除按钮
        self.DelButton.setStyleSheet(
            '''QPushButton{background:%s;color:%s;border-radius: 7px;}
            QPushButton:hover{background:rgb(244,71,53);color:%s;border-radius: 7px;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))

    def show(self):
        self.SetUp()
        super(DisplayInfoWindowSamllImg, self).show()

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()

# 展示、修改信息窗口(图片格式格式)
class DisplayInfoWindowBigImg(EnbuBasicWindow):
    def __init__(self, name, dad, data):
        super(DisplayInfoWindowBigImg, self).__init__()
        self.Theme = dad.Theme  # 储存深浅色
        self.dad = dad
        self.data = data
        self.ChildWindow = None  # 子窗口打开情况
        self.resize(450, 500)  # 尺寸

    def UIinit(self):
        self.Theme = self.dad.Theme
        self.BackGround  = QLabel('', self)         # 背景
        self.MiniButton  = QPushButton('', self)    # 最小化按钮
        self.CloseButton = QPushButton('', self)    # 关闭按钮
        self.ResizeBtn   = MoveButton('', self)     # 缩放按钮
        self.Title       = QLabel('', self)         # 标题

        self.ImgShow         = ImgInputAndShowAutoResize('', self)  # 图片显示
        self.Container       = ShowContainerBar('', self) # 一个容器
        self.TextBox         = TextBox('', self)  # 显示仓库信息文本

        self.DelButton    = QPushButton('', self)  # 删除按钮
        self.FinishButton = QPushButton('', self)  # 保存按钮

    def UIcss(self):
        # 根据深浅色选择一个配置
        temp_qss = DayQss if self.Theme == "Day" else NightQss

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

        # 更改文本
        self.TextBox.text1.setText(self.dad.dad.dad.now_class.name)
        self.TextBox.text2.setText(self.dad.dad.dad.now_class.create_time)
        self.TextBox.text3.setText(self.dad.dad.dad.now_class.remarks)

        self.DelButton.setText("")
        self.DelButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.DelButton.setStyleSheet(
            '''QPushButton{background:%s;color:%s;border-radius: 7px;}
            QPushButton:hover{background:rgb(244,71,53);color:%s;border-radius: 7px;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.font_color1))
        self.DelButton.setMinimumWidth(140)

        # 完成按钮
        self.FinishButton.setFont(QtGui.QFont("arial", AllQss.font_size + 20))
        self.FinishButton.setText(QtCore.QCoreApplication.translate("MainWindow", "ok"))
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))
        self.FinishButton.setGraphicsEffect(self.Get_Shaow())

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

        # 标题
        self.Title.setGeometry(QtCore.QRect(k + 7, k + 5, 100, 20))

        # 图片显示
        self.ImgShow.move(k + 20, k + 25)
        self.ImgShow.AutoResize()

        # 容器
        self.Container.setGeometry(QtCore.QRect(k + 5, self.ImgShow.height() + k + 30,
                                                self.width() - 2 * k - 20,
                                                self.height() - k - 20 - (self.ImgShow.height() + k + 30)))

        # 放置控件
        self.Container.layout.addWidget(self.TextBox)  # 加入文本
        i = 0
        for name in SQLopt.GetTableName(self.dad.dad.dad.cur, self.dad.dad.dad.now_class.name)[:-1]:
            if name == "图片":
                self.ImgShow.SetImg(self.data[i])
                i += 1
                continue
            temp = TextInput(name, self)
            temp.Input.setText(self.data[i])
            i += 1
            self.Container.layout.addWidget(temp)

        self.Container.layout.addWidget(self.DelButton, 1, Qt.AlignHCenter)  # 删除按钮
        self.Container.layout.addWidget(EmptBox('', self))  # 加入一个空的

        # 完成按钮
        self.FinishButton.setGeometry(QtCore.QRect(self.width() - 100 - 25, self.height() - 110 - 25, 60, 60))

    def UIfun(self):
        # 关闭按钮
        def ClossAll():
            self.dad.dad.DispalyIndoWindowList.remove(self.dad.DisPlayWindow)
            self.dad.DisPlayWindow = None
            self.close()
        self.CloseButton.clicked.connect(ClossAll)

        # 最小按钮
        self.MiniButton.clicked.connect(lambda x: self.showMinimized())

        self.ResizeBtn.siteChanged.connect(self.ResizeWindow)

        # 编辑完成
        def InputFinish():
            data = []
            # 遍历子控件
            for i in range(1, self.Container.layout.count() - 2):
                if i == 1:
                    data.append(self.Container.layout.itemAt(i).widget().GetText())
                    data.append(self.ImgShow.path)
                    continue
                data.append(self.Container.layout.itemAt(i).widget().GetText())

            # 检查输入是否合格
            if not CheckAddInfo(self, data):
                return

            # 检查输入是否有改变
            different_text = ShowDifferent(SQLopt.GetTableName(self.dad.dad.dad.cur,
                                                 self.dad.dad.dad.now_class.name),
                             self.data,
                             data)
            if different_text:
                def fun_true():
                    # 添加进数据库
                    data.append(GetAllTime())
                    SQLopt.ReplaceRow(self.dad.dad.dad.conn,
                                      self.dad.dad.dad.cur,
                                      self.dad.dad.dad.now_class.name,
                                      SQLopt.GetTableName(self.dad.dad.dad.cur,
                                                          self.dad.dad.dad.now_class.name),
                                      self.data,
                                      data)

                    ClossAll()
                    self.dad.dad.dad.Container.UpdataContainer(self.dad.dad.dad.now_class.name)  # 更新右边的容器

                    # 弹出提示
                    AlertWindow(self, "🥳", "<%s>更新成功！" % (data[0])).show()

                QuestionWindow(self, "🧐", "您确定更新吗\n\n" + different_text, lambda :None, fun_true).show()

            else:
                ClossAll()



        self.FinishButton.clicked.connect(InputFinish)

        # 删除信息
        def DelInfo():
            def fun_true():
                # 从数据库中删除
                SQLopt.DelereRow(self.dad.dad.dad.conn, self.dad.dad.dad.cur,
                                self.dad.dad.dad.now_class.name,
                                SQLopt.GetTableName(self.dad.dad.dad.cur, self.dad.dad.dad.now_class.name),
                                self.data)

                # 从布局中移除要删除的控件
                try:
                    self.dad.dad.dad.Container.layout.removeWidget(self.dad)
                    self.dad.setVisible(False)  # 隐藏控件
                except:
                    self.dad.dad.dad.Container.UpdataContainer(self.dad.dad.dad.now_class.name)

                ClossAll()  # 关闭控件
                QCoreApplication.processEvents()  # 强制处理事件队列，立即更新界面

            QuestionWindow(self, "🥲", "<这个操作是不可逆转的>\n真的要删除 %s的 \n %s 吗？" % (self.dad.dad.dad.now_class.name, self.data[0]),
                           lambda: None, fun_true).show()

        self.DelButton.clicked.connect(DelInfo)

    # 缩放界面
    def ResizeWindow(self):
        k = 25
        w, h = self.ResizeBtn.x() + k + 35, self.ResizeBtn.y() + k + 35
        self.resize(w, h)  # 总窗口尺寸

        self.BackGround.setGeometry(QtCore.QRect(20, 20, self.width() - 2 * k, self.height() - 2 * k))
        self.MiniButton.setGeometry(QtCore.QRect(self.width() - 75 - k, k - 7, 30, 30))  # 最小化按钮
        self.CloseButton.setGeometry(QtCore.QRect(self.width() - 45 - k, k - 5, 30, 30))  # 关闭
        # 图片显示
        self.ImgShow.AutoResize()
        # 容器
        self.Container.setGeometry(QtCore.QRect(k + 5, self.ImgShow.height() + k + 30,
                                                self.width() - 2 * k - 20,
                                                self.height() - k - 20 - (self.ImgShow.height() + k + 30)))
        self.FinishButton.setGeometry(QtCore.QRect(self.width() - 100 - 25, self.height() - 110 - 25, 60, 60))  # 完成按钮

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

        # 文本
        self.TextBox.SetDay()

        # 容器
        self.Container.SetDay()

        # 删除按钮
        self.DelButton.setStyleSheet(
            '''QPushButton{background:%s;color:%s;border-radius: 7px;}
            QPushButton:hover{background:rgb(244,71,53);color:%s;border-radius: 7px;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))

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

        # 文本
        self.TextBox.SetNight()

        # 容器
        self.Container.SetNight()

        # 删除按钮
        self.DelButton.setStyleSheet(
            '''QPushButton{background:%s;color:%s;border-radius: 7px;}
            QPushButton:hover{background:rgb(244,71,53);color:%s;border-radius: 7px;}''' %
            (temp_qss.fill_color1, temp_qss.font_color1, temp_qss.font_color1))

        # 完成按钮
        self.FinishButton.setStyleSheet(
            '''QPushButton{background:%s;border-radius: 30px;border: 0px;color: %s;font-weight: bold;}
            QPushButton:hover{background:%s;border-radius: 30px;border: 5px solid %s;color: %s;font-weight: bold;}''' %
            (temp_qss.theme_color, "#ffffff", temp_qss.theme_color, "#ffffff", "#ffffff"))

    def show(self):
        self.SetUp()
        super(DisplayInfoWindowBigImg, self).show()

    # 加载东西
    def SetUp(self):
        self.UIinit()
        self.UIcss()
        self.UIsite()
        self.UIfun()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DisplayInfoWindow()  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程