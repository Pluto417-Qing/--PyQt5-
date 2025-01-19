from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from Ui_MainWindow import Ui_MainWindow
from CallTomatoWindow import tomatoWindow
from CallTaskWindow import taskWindow
from CallHistoryWindow import HistoryWindow
from datetime import datetime

def time_calculator(time):
    """
    该函数负责处理时钟显示的时间，将显示的时间转化为以分钟为单位的值
    """
    hours, minutes, seconds = map(int, time.split(':')) # 时钟显示的时间格式为 "HH:MM:SS"
    total_minutes = hours * 60 + minutes + seconds / 60  # 计算总分钟数
    return total_minutes  # 返回总分钟数

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    这是应用的主窗口，包含了应用的主逻辑，从该窗口通过按键调用其他窗口。
    该窗口同时也负责数据的处理，比如历史记录的提取与分类。
    """
    ongoingTask = ""

    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)

        self.setGeometry(1000, 400, 511, 741)  # 设置窗口位置和大小
        self.setupUi(self)      # 初始化程序界面
        self.setWindowTitle("小黄人时间管理器")  # 设置窗口标题

        self.myTaskWindow = taskWindow()    # 建立任务窗口
        self.myTomatoWindow = tomatoWindow()    # 建立番茄钟窗口
        self.myHistoryWindow = HistoryWindow()  # 建立历史记录窗口

        self.timeing = QTimer()     # 建立计时器
        self.timeing.setInterval(1000)  # 设置刷新计时器的时间间隔为1秒

        self.isTiming = False   # 标志：是否正在计时
        # 信号与槽的连接,按下相应的按钮执行相应的功能
        self.startTiming.clicked.connect(self.timerManage)
        self.callTomatoWindowButton.clicked.connect(self.callMyTomatoWindow)
        self.callTaskWIndowButton.clicked.connect(self.callMyTaskWindow)
        self.readHistoryButton.clicked.connect(self.callMyHistoryWindow)
        self.myTaskWindow.task_signal.connect(self.startTaskTiming)
        self.endTaskButton.clicked.connect(self.endTaskTiming)
        self.resetButton.clicked.connect(self.resetTimer)

    def timerManage(self):
        """
        时间管理函数
        """
        if not self.isTiming:
            # 如果原来没有在计时，则开始计时
            self.isTiming = True
            self.timeing.start()
            self.timeing.timeout.connect(self.timerUpdate)
        else:
            # 如果原来正在计时，则暂停计时
            self.isTiming = False
            self.timeing.stop()
            self.timeing.timeout.disconnect(self.timerUpdate)

    def resetTimer(self):
        # 计时器归零
        self.Timer.setText("00:00:00")
        if self.isTiming:
            self.isTiming = False
            self.timeing.timeout.disconnect(self.timerUpdate)

    def timerUpdate(self):
        """
        更新计时器
        """
        pre_text = self.Timer.text()
        hours, minutes, seconds = map(int, pre_text.split(':'))
        new_seconds = (seconds + 1) % 60
        new_minutes = (minutes + (seconds + 1) // 60) % 60
        new_hours = (hours + (minutes + (seconds + 1) // 60) // 60) % 24

        show_hours = f'{new_hours:02}'
        show_minutes = f'{new_minutes:02}'
        show_seconds = f'{new_seconds:02}'

        show_time = ':'.join([show_hours, show_minutes, show_seconds])
        self.Timer.setText(show_time)

    def callMyTomatoWindow(self):
        self.myTomatoWindow.show()

    def callMyTaskWindow(self):
        self.myTaskWindow.show()

    def callMyHistoryWindow(self):
        self.myHistoryWindow.loadHistory()
        self.myHistoryWindow.show()

    def startTaskTiming(self,taskText):
        self.timerManage()
        self.ongoingTask = taskText

    def endTaskTiming(self):
        time = self.Timer.text()  # 获取当前计时器的内容
        task_time = time_calculator(time)  # 获取总任务时间
        self.resetTimer()
        self.ongoingTask += f"   时间: {task_time:.2f} 分钟"

        # 获取当前日期
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化日期

        # 追加日期信息
        self.ongoingTask += f"   日期: {current_date}"

        with open("history.txt", 'a') as f:     # 写入一条历史记录
            f.write(self.ongoingTask + "\n")