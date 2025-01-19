from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QVBoxLayout, QListWidget, QWidget
from Ui_historyWindow import Ui_HistoryWindow
from datetime import datetime
from matplotlib import pyplot as plt
import os
plt.rcParams['font.sans-serif']=['SimHei']  #解决中文乱码

class Tab:
    def __init__(self,name):
        self.name = name  # 名称
        self.taskList = []
        self.tab_layout = QVBoxLayout()
        self.list_widget = QListWidget()

class Task:
    def __init__(self,name,kind,time,note="无",endurance=0.0):
        self.name = name  # 名称
        self.kind = kind  # 类型
        self.note = note  # 备注
        self.time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')  # 创建时间转为datetime对象
        self.endurance = endurance

class HistoryWindow(QMainWindow, Ui_HistoryWindow):
    history = []            # 存储从文件读取的历史记录
    taskList = []           # 任务列表，元素类型为Task类
    dateList = dict()       # 按日期记录任务时间
    kindList = dict()       # 按类别记录任务时间

    def __init__(self, parent: object = None) -> None:
        super(HistoryWindow, self).__init__(parent)

        self.setGeometry(1000, 400, 511, 741)  # 设置窗口位置和大小
        self.setupUi(self)  # setup UI
        self.setWindowTitle("查看历史记录")
        #self.loadHistory()  # 载入历史记录

        self.clearHistoryButton.clicked.connect(self.clearHistory)

    def loadHistory(self):
        self.processHistory()
        # 更新列表显示
        self.showHistoryLW.clear()  # 清空已有的显示
        for task in self.taskList:
            line = f"任务名称: {task.name}  类型: {task.kind} 时间: {task.time.strftime('%Y-%m-%d %H:%M:%S')} 执行时间: {task.endurance:1.2f} 分钟 备注: {task.note}"
            new_item = QListWidgetItem(line.strip())
            self.showHistoryLW.addItem(new_item)

        self.statisticsShow()
        self.kindTabProcess()
        self.plotDraw()

    def clearHistory(self):
        # 清空历史记录列表
        self.showHistoryLW.clear()  # 清空ListWidget中的所有项
        self.historyStatisticLW.clear()
        self.kindTab.clear()
        self.plotCanvas.clear()
        # 清空文件内容
        with open("history.txt", 'w') as f:  # 以写模式打开文件
            f.write("")  # 写入空字符串

    def processHistory(self):
        self.history = []
        self.taskList = []
        self.dateList = dict()
        self.kindList = dict()

        file_path = "history.txt"
        # 判断文件是否存在
        if not os.path.exists(file_path):
            # 如果文件不存在，创建文件
            with open(file_path, 'w') as file:
                file.write('')  # 创建空文件

        with open("history.txt", 'r') as file:
            for line in file:
                parts = line.strip().split('   ')  # 去掉行首尾空白字符
                filtered_parts = [item.strip() for item in parts if item.strip()]
                name = filtered_parts[0].strip().split(':')[1].strip()
                kind = filtered_parts[1].strip().split(':')[1].strip()
                note = filtered_parts[2].strip().split(':')[1].strip()
                endurance = float(filtered_parts[3].strip().split(' ')[1].strip())
                time = filtered_parts[4].strip().split(':',1)[1].strip()
                if kind not in self.kindList.keys():
                    self.kindList[kind] = endurance
                else:
                    self.kindList[kind] += endurance
                if time.split(" ")[0] not in self.dateList.keys():
                    self.dateList[time.split(" ")[0]] = endurance
                else:
                    self.dateList[time.split(" ")[0]] += endurance
                new_task = Task(name,kind,time,note,endurance)
                self.taskList.append(new_task)

        # 按日期排序
        self.taskList.sort(key=lambda task: task.time)  # 按时间属性排序

    def statisticsShow(self):
        self.historyStatisticLW.clear()
        for date in self.dateList.keys():
            line = f"日期: {date.split(' ')[0]}  任务时长: {self.dateList[date]:1.2f} 分钟"
            new_item = QListWidgetItem(line)
            self.historyStatisticLW.addItem(new_item)

    def kindTabProcess(self):
        self.kindTab.clear()
        for tab in self.kindList.keys():
            new_tab = Tab(tab)
            newTabWidget = QWidget()  # 创建 QWidget 作为标签页
            newTabWidget.setLayout(new_tab.tab_layout)  # 设置布局
            #new_tab.tab_layout.addWidget(new_tab.list_widget)  # 将 QListWidget 添加到布局
            self.kindTab.addTab(newTabWidget, tab)  # 将新标签页添加到 tab

            # 添加任务到该类别的 QListWidget
            for task in self.kindList.keys():
                if task == tab:
                    # print(self.kindList[tab])
                    new_item = QListWidgetItem(str(self.kindList[task])+"分钟")  # 使用任务名称
                    new_tab.list_widget.addItem(new_item)
                    new_tab.tab_layout.addWidget(new_tab.list_widget)  # 将 QListWidget 添加到布局

    def plotDraw(self):
        plt.figure(figsize=(5, 5))  # 将画布设定为正方形，则绘制的饼图是正圆
        label = self.kindList.keys()    #定义饼图的标签
        explode = [0.01] * len(label)  # 设定各项距离圆心n个半径
        values = self.kindList.values()

        plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')  # 绘制饼图
        plt.title('任务分布占比图')  # 绘制标题
        plt.savefig('./任务分布占比图.png')  # 保存图片
        plt.close()

        self.plotCanvas.setStyleSheet("""
            QLabel {
            background-image: url(./任务分布占比图.png);  
            background-repeat: no-repeat;       /* 不重复 */
            background-position: center;        /* 居中 */
            background-attachment: fixed;       /* 固定背景 */
        }
        """)