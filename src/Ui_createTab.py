# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_createTab(object):
  def setupUi(self, createTab):
    createTab.setObjectName("createTab")
    createTab.resize(342, 169)
    self.tabInput = QtWidgets.QLineEdit(createTab)
    self.tabInput.setGeometry(QtCore.QRect(100, 90, 141, 31))
    self.tabInput.setObjectName("tabInput")
    self.listView_2 = QtWidgets.QListView(createTab)
    self.listView_2.setGeometry(QtCore.QRect(-40, -20, 411, 241))
    self.listView_2.setStyleSheet("border-image:url(:/background/resource/background/bg1.jpg)")
    self.listView_2.setObjectName("listView_2")
    self.sureButton = QtWidgets.QPushButton(createTab)
    self.sureButton.setGeometry(QtCore.QRect(130, 130, 75, 24))
    self.sureButton.setObjectName("sureButton")
    self.listView_2.raise_()
    self.tabInput.raise_()
    self.sureButton.raise_()

    self.retranslateUi(createTab)
    QtCore.QMetaObject.connectSlotsByName(createTab)

  def retranslateUi(self, createTab):
    _translate = QtCore.QCoreApplication.translate
    createTab.setWindowTitle(_translate("createTab", "Dialog"))
    self.sureButton.setText(_translate("createTab", "确定"))
import resource_rc


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  createTab = QtWidgets.QDialog()
  ui = Ui_createTab()
  ui.setupUi(createTab)
  createTab.show()
  sys.exit(app.exec_())
