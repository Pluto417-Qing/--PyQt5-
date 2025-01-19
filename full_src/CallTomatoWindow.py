from PyQt5.QtWidgets import QMainWindow, QMessageBox
from Ui_tomatoWindow import Ui_tomatoWindow
from PyQt5.QtCore import QTimer

class tomatoWindow(QMainWindow, Ui_tomatoWindow):
    def __init__(self, parent: object = None) -> None:
        super(tomatoWindow, self).__init__(parent)

        self.remainingTime = 0  # 剩余时间
        self.setGeometry(1000, 400, 511, 741)  # 设置窗口位置和大小
        self.setupUi(self)
        self.setWindowTitle("番茄钟")

        self.tomatoTimer = QTimer()
        self.tomatoTimer.setInterval(1000)  # 每秒触发一次
        self.tomatoTimer.timeout.connect(self.updateTiming)  # 连接超时信号

        self.isTomatoTiming = False
        self.startTomato.clicked.connect(self.manageTiming)  # 连接按钮点击信号

    def manageTiming(self):
        if not self.isTomatoTiming:
            self.isTomatoTiming = True
            self.remainingTime = self.readTime() * 60  # 转换为秒
            show_minutes = self.remainingTime // 60
            show_seconds = self.remainingTime % 60
            self.tomatoTimeBoard.setText(f'{show_minutes:02}:{show_seconds:02}')
            self.tomatoTimer.start()
        else:
            self.isTomatoTiming = False
            self.tomatoTimer.stop()

    def updateTiming(self):
        if self.remainingTime > 0:
            self.remainingTime -= 1
            show_minutes = self.remainingTime // 60
            show_seconds = self.remainingTime % 60
            self.tomatoTimeBoard.setText(f'{show_minutes:02}:{show_seconds:02}')
        else:
            self.tomatoTimer.stop()
            self.alert()
            self.isTomatoTiming = False

    def readTime(self) -> int:
        if self.editTomato.value():
            value = self.editTomato.value()
            self.editTomato.setValue(0)
            return int(value)
        elif self.tomato10.isChecked():
            return 10
        elif self.tomato20.isChecked():
            return 20
        elif self.tomato30.isChecked():
            return 30
        elif self.tomato45.isChecked():
            return 45
        else:
            return 0

    def alert(self):
        QMessageBox.warning(self, '提示', '时间到!')
