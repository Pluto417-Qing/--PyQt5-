from PyQt5.QtWidgets import QDialog
from Ui_taskCreator import Ui_createTaskDialog

class createTaskDialog(QDialog, Ui_createTaskDialog):
    def __init__(self, parent: object = None) -> None:
        super(createTaskDialog, self).__init__(parent)

        self.setGeometry(1000, 400, 511, 741)  # 设置窗口位置和大小
        self.setupUi(self)  # 初始化界面
        self.setWindowTitle("创建任务") # 设置窗口标题

