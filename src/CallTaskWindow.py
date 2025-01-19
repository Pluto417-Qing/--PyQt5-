from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QListWidget, QVBoxLayout, QListWidgetItem
from CallTaskCreator import createTaskDialog
from Ui_taskWindow import Ui_taskWindow
from datetime import datetime
from CallCreateTab import createTab

class Task:
    def __init__(self,name,kind,note,time,endurance=0):
        self.name = name  # 名称
        self.kind = kind  # 类型
        self.note = note  # 备注
        self.time = time  # 创建时间
        self.endurance = 0 # 执行时间

class Tab:
    def __init__(self,name):
        self.name = name  # 名称
        self.taskList = []
        self.tab_layout = QVBoxLayout()
        self.list_widget = QListWidget()

def get_add_line(new_task):
    return (f"任务名称: {new_task.name:<10}   "
            f"类别: {new_task.kind:<10}   "
            f"备注: {new_task.note:<10}")

class taskWindow(QMainWindow, Ui_taskWindow):
    # taskList = []
    tabList = []
    nameList = ["数学", "英语", "编程", "运动"]
    task_signal = pyqtSignal(str)  # 定义一个信号，传递一个字符串

    def __init__(self, parent: object = None) -> None:
        super(taskWindow, self).__init__(parent)

        self.setGeometry(1000, 400, 511, 741)  # 设置窗口位置和大小
        self.setupUi(self)
        self.setWindowTitle("任务管理器")

        self.myDialog = createTaskDialog()
        self.init_default_creator()
        self.myCreateTabDialog = createTab()
        self.init_default_tab()

        self.createTaskButton.clicked.connect(self.showMyDialog)
        self.createTabButton.clicked.connect(self.showCreateTabDialog)
        self.delTaskButton.clicked.connect(self.del_task)
        self.startTaskButton.clicked.connect(self.start_task)

    def showMyDialog(self):
        #self.myDialog.sureButton.clicked.disconnect()
        self.myDialog.show()
        self.myDialog.sureButton.clicked.connect(self.process_task_input)

    def process_task_input(self):
        input_kind = self.myDialog.taskKind.currentText()
        input_name = self.myDialog.taskName.text()
        input_note = self.myDialog.taskNote.toPlainText()
        current_time = datetime.now()

        new_task = Task(input_name,input_kind,input_note,current_time)
        # self.taskList.append(new_task)
        self.updateTaskList(new_task)

        self.myDialog.close()
        QMessageBox.warning(self, '提示', '创建成功')
        self.myDialog.sureButton.clicked.disconnect(self.process_task_input)  # 断开之前的连接

    def showCreateTabDialog(self):
        #self.myCreateTabDialog.sureButton.clicked.disconnect()  # 断开之前的连接
        self.myCreateTabDialog.show()
        self.myCreateTabDialog.sureButton.clicked.connect(self.process_tab_input)

    def process_tab_input(self):
        newTabWidget = QWidget()
        tab_text = self.myCreateTabDialog.tabInput.text()
        new_tab = Tab(tab_text)

        self.taskTab.addTab(newTabWidget,tab_text)
        newTabWidget.setLayout(new_tab.tab_layout)
        new_tab.tab_layout.addWidget(new_tab.list_widget)

        self.myDialog.taskKind.addItem(tab_text)

        self.tabList.append(new_tab)
        self.nameList.append(tab_text)
        self.myCreateTabDialog.close()
        self.myCreateTabDialog.sureButton.clicked.disconnect(self.process_tab_input)  # 断开之前的连接

    def updateTaskList(self,new_task):
        # 设置标签页的布局和内容
        # print(self.tabList)
        for tab in self.tabList:
            if tab.name == new_task.kind:
                new_item = QListWidgetItem(get_add_line(new_task))
                tab.list_widget.addItem(new_item)
                tab.taskList.append(new_task)
                #tab.list_widget.setLayout(tab.tab_layout)

    def init_default_tab(self):
        for tab in self.nameList:
            new_tab = Tab(tab)
            newTabWidget = QWidget()  # 创建 QWidget 作为标签页
            newTabWidget.setLayout(new_tab.tab_layout)  # 设置布局
            new_tab.tab_layout.addWidget(new_tab.list_widget)  # 将 QListWidget 添加到布局
            self.tabList.append(new_tab)
            self.taskTab.addTab(newTabWidget, tab)  # 将新标签页添加到 tab

    def init_default_creator(self):
        self.myDialog.taskKind.addItems(self.nameList)

    def del_task(self):
        index = self.taskTab.currentIndex()  # 获取当前选中的标签页索引
        tab_name = self.taskTab.tabText(index)  # 获取当前标签页名称

        for tab in self.tabList:
            if tab.name == tab_name:
                selected_row = tab.list_widget.currentRow()  # 获取当前选中项的行号
                if selected_row != -1:  # 确保有选中的项
                    # 删除选中的任务项
                    tab.list_widget.takeItem(selected_row)
                    QMessageBox.warning(self, '提示', '删除成功')
                else:
                    QMessageBox.warning(self, '提示', '请先选择要删除的任务')

    def start_task(self):
        index = self.taskTab.currentIndex()  # 获取当前选中的标签页索引
        tab_name = self.taskTab.tabText(index)  # 获取当前标签页名称

        for tab in self.tabList:
            if tab.name == tab_name:
                selected_row = tab.list_widget.currentRow()  # 获取当前选中项的行号
                if selected_row != -1:  # 确保有选中的项
                    selected_item = tab.list_widget.item(selected_row)  # 获取选中的项
                    task_content = selected_item.text()  # 获取选中项的文本
                    self.task_signal.emit(task_content)  # 发射信号
                    self.close()
                else:
                    QMessageBox.warning(self, '提示', '请先选择要处理的任务')





