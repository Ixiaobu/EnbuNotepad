from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QColor
from PyQt5 import QtCore, QtWidgets

class EnbuBasicWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(EnbuBasicWindow, self).__init__()
        self.centralwidget = QtWidgets.QWidget(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 去掉窗口标题栏和按钮, 使窗口置顶， 使窗口不显示在任务栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口真透明
        self.m_flag = True

    # =======窗口移动相关=======
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            try:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()
                self.change_window_emit(self.x(), self.y())
            except:
                return

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    # =======窗口移动相关=======

    # 背景阴影
    def Get_Shaow(self):
        shadow = QGraphicsDropShadowEffect(self)  # 创建阴影
        shadow.setColor(QColor(0,0,0,100))  # 设置阴影颜色为红色
        shadow.setBlurRadius(23)  # 设置阴影大小为9px
        shadow.setOffset(0, 0)  # 阴影偏移距离为0px
        return shadow