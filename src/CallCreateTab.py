from PyQt5.QtWidgets import QDialog
from Ui_createTab import Ui_createTab


class createTab(QDialog, Ui_createTab):
    def __init__(self, parent: object = None) -> None:
        super(createTab, self).__init__(parent)

        self.setupUi(self)  # 初始化程序界面
        self.setWindowTitle("创建新的任务分类")  # 设置窗口标题


