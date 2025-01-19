import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from CallMainWindow import MainWindow
from CallWelcomeWindow import WelcomeWindow 

def main():
    """
    该函数为应用的入口函数，主要负责建立app运行的循环
    和进入应用时的欢迎界面与主界面
    """
    app = QApplication(sys.argv)
    
    mainWindow = MainWindow()       # 建立主界面
    welcomeWindow = WelcomeWindow()     # 建立欢迎界面
    
    welcomeWindow.show()
    QTimer.singleShot(3000, welcomeWindow.close) # 设置定时器，3秒后关闭欢迎窗口
    QTimer.singleShot(3000, mainWindow.show) # 设置定时器，3秒后显示主窗口

    sys.exit(app.exec())    # 进入循环

if __name__ == "__main__":
    main()

