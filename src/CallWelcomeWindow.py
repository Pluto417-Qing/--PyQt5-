from PyQt5.QtWidgets import QMainWindow
from Ui_WelcomeWindow import Ui_WelcomeWindow

class WelcomeWindow(QMainWindow, Ui_WelcomeWindow):
    def __init__(self, parent: object = None) -> None:
        super(WelcomeWindow,self).__init__(parent)
       
        self.setGeometry(1000, 400, 511, 741)  # 设置窗口位置和大小
        self.setupUi(self)
        self.setWindowTitle("小黄人时间管理器")


