import sys, threading

import serial
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import utils
import UI_realtime
from PIL import Image
import numpy as np


# 初始化多线程
class thread_UI(threading.Thread):
    def run(self):
        main()


thread_UI = thread_UI()  # 界面主线程


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.END = False
        self.openCom_succeed = 0
        self.openCom_faild = 0
        self.thread_begin_Measure = Ui_MainWindow.thread_begin_Measure()
        self.beginMeasure_i = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_treadAll = QtWidgets.QLabel(self.centralwidget)
        self.label_treadAll.setGeometry(QtCore.QRect(160, 0, 561, 181))
        self.label_treadAll.setObjectName("label_treadAll")
        self.label_tread1 = QtWidgets.QLabel(self.centralwidget)
        self.label_tread1.setGeometry(QtCore.QRect(160, 210, 271, 111))
        self.label_tread1.setObjectName("label_tread1")
        self.label_tread2 = QtWidgets.QLabel(self.centralwidget)
        self.label_tread2.setGeometry(QtCore.QRect(450, 210, 271, 111))
        self.label_tread2.setObjectName("label_tread2")
        self.label_tread3 = QtWidgets.QLabel(self.centralwidget)
        self.label_tread3.setGeometry(QtCore.QRect(160, 340, 271, 111))
        self.label_tread3.setObjectName("label_tread3")
        self.label_tread4 = QtWidgets.QLabel(self.centralwidget)
        self.label_tread4.setGeometry(QtCore.QRect(450, 340, 271, 111))
        self.label_tread4.setObjectName("label_tread4")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 82, 381))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_openCom = QtWidgets.QPushButton(self.layoutWidget)
        self.button_openCom.setObjectName("button_openCom")
        self.verticalLayout.addWidget(self.button_openCom)
        self.button_beginMeasure = QtWidgets.QPushButton(self.layoutWidget)
        self.button_beginMeasure.setObjectName("button_beginMeasure")
        self.verticalLayout.addWidget(self.button_beginMeasure)
        self.button_stopMeasure = QtWidgets.QPushButton(self.layoutWidget)
        self.button_stopMeasure.setObjectName("button_stopMeasure")
        self.verticalLayout.addWidget(self.button_stopMeasure)
        self.button_showTreadAll = QtWidgets.QPushButton(self.layoutWidget)
        self.button_showTreadAll.setObjectName("button_showTreadAll")
        self.verticalLayout.addWidget(self.button_showTreadAll)
        self.button_showTread1 = QtWidgets.QPushButton(self.layoutWidget)
        self.button_showTread1.setObjectName("button_showTread1")
        self.verticalLayout.addWidget(self.button_showTread1)
        self.button_showTread2 = QtWidgets.QPushButton(self.layoutWidget)
        self.button_showTread2.setObjectName("button_showTread2")
        self.verticalLayout.addWidget(self.button_showTread2)
        self.button_showTread3 = QtWidgets.QPushButton(self.layoutWidget)
        self.button_showTread3.setObjectName("button_showTread3")
        self.verticalLayout.addWidget(self.button_showTread3)
        self.button_showTread4 = QtWidgets.QPushButton(self.layoutWidget)
        self.button_showTread4.setObjectName("button_showTread4")
        self.verticalLayout.addWidget(self.button_showTread4)
        self.button_slideTableRun = QtWidgets.QPushButton(self.layoutWidget)
        self.button_slideTableRun.setObjectName("slideTableRun")
        self.verticalLayout.addWidget(self.button_slideTableRun)
        self.button_slideTableStop = QtWidgets.QPushButton(self.layoutWidget)
        self.button_slideTableStop.setObjectName("slideTableStop")
        self.verticalLayout.addWidget(self.button_slideTableStop)
        self.button_exit = QtWidgets.QPushButton(self.layoutWidget)
        self.button_exit.setObjectName("button_exit")
        self.verticalLayout.addWidget(self.button_exit)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(150, 465, 591, 111))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 信号槽
        self.button_openCom.clicked.connect(self.openCom)
        self.button_beginMeasure.clicked.connect(self.beginMeasure)
        # self.button_stopMeasure.clicked.connect(self.stopMeasure)
        self.button_showTreadAll.clicked.connect(self.showTreadAll)
        self.button_showTread1.clicked.connect(self.showTread1)
        self.button_showTread2.clicked.connect(self.showTread2)
        self.button_showTread3.clicked.connect(self.showTread3)
        self.button_showTread4.clicked.connect(self.showTread4)
        self.button_slideTableRun.clicked.connect(self.slideTableRun)
        self.button_slideTableStop.clicked.connect(self.slideTableStop)
        self.button_exit.clicked.connect(QCoreApplication.instance().quit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_treadAll.setText(_translate("MainWindow", "treadAll"))
        self.label_tread1.setText(_translate("MainWindow", "tread1"))
        self.label_tread2.setText(_translate("MainWindow", "tread2"))
        self.label_tread3.setText(_translate("MainWindow", "tread3"))
        self.label_tread4.setText(_translate("MainWindow", "tread4"))
        self.button_openCom.setText(_translate("MainWindow", "打开串口"))
        self.button_beginMeasure.setText(_translate("MainWindow", "开始测量"))
        self.button_stopMeasure.setText(_translate("MainWindow", "停止测量"))
        self.button_showTreadAll.setText(_translate("MainWindow", "显示轮胎胎面"))
        self.button_showTread1.setText(_translate("MainWindow", "显示花纹1"))
        self.button_showTread2.setText(_translate("MainWindow", "显示花纹2"))
        self.button_showTread3.setText(_translate("MainWindow", "显示花纹3"))
        self.button_showTread4.setText(_translate("MainWindow", "显示花纹4"))
        self.button_slideTableRun.setText(_translate("MainWindow", "开启滑台"))
        self.button_slideTableStop.setText(_translate("MainWindow", "停止滑台"))
        self.button_exit.setText(_translate("MainWindow", "退出"))

    def openCom(self):
        a = utils.openCom()
        if a:
            QMessageBox.information(self, "串口", "开启串口成功",
                                    QMessageBox.Yes)
            self.openCom_succeed += 1
            self.openCom_faild = 0
        elif self.openCom_succeed > 0 and self.openCom_faild == 0:
            QMessageBox.information(self, "串口", "已开启串口，请勿重复点击",
                                    QMessageBox.Yes)
        else:
            QMessageBox.information(self, "串口", "开启串口失败，请检查串口连接",
                                    QMessageBox.Yes)
            self.openCom_faild += 1

    class thread_begin_Measure(threading.Thread):
        def run(self):
            Ui_MainWindow().beginMeasure()

    def beginMeasure(self):  # 包括了测量部分、实时显示部分、计算部分、保存图片部分、显示结果到窗口部分
        self.beginMeasure_i += 1
        if self.beginMeasure_i == 1:
            utils.thread_init.start()
            utils.thread_init.join()
            utils.thread_openSlide.start()
            utils.thread_openSlide.join()
            # 开始测量
            self.child_window = UI_realtime.MainUi()
            self.child_window.show()
        else:
            QMessageBox.information(self, "警告", "请等待本次测量结束",
                                    QMessageBox.Yes)

    def showResult(self):
        result = np.loadtxt('result.txt')
        result = list(result)
        for i in range(len(result)):
            Ui_MainWindow.printf(self, "第" + str(i + 1) + "个轮胎花纹深度为：" + str(round(result[i], 4)) + "mm")
        self.beginMeasure_i = 0

    def printf(self, mes):
        self.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursot.End)
        QtWidgets.QApplication.processEvents()

    def showTread1(self):
        img = Image.open('tread1.png')
        img1 = img.resize((self.label_tread1.width(), self.label_tread1.height()))
        img1.save('tread1.png')
        self.label_tread1.setPixmap(QPixmap('tread1.png'))

    def showTread2(self):
        img = Image.open('tread2.png')
        img1 = img.resize((self.label_tread2.width(), self.label_tread2.height()))
        img1.save('tread2.png')
        self.label_tread2.setPixmap(QPixmap('tread2.png'))

    def showTread3(self):
        img = Image.open('tread3.png')
        img1 = img.resize((self.label_tread3.width(), self.label_tread3.height()))
        img1.save('tread3.png')
        self.label_tread3.setPixmap(QPixmap('tread3.png'))

    def showTread4(self):
        img = Image.open('tread4.png')
        img1 = img.resize((self.label_tread4.width(), self.label_tread4.height()))
        img1.save('tread4.png')
        self.label_tread4.setPixmap(QPixmap('tread4.png'))

    def showTreadAll(self):
        img = Image.open('treadAll.png')
        img1 = img.resize((self.label_treadAll.width(), self.label_treadAll.height()))
        img1.save('treadAll.png')
        self.label_treadAll.setPixmap(QPixmap('treadAll.png'))

    def slideTableRun(self):
        utils.slideTableRun()

    def slideTableStop(self):
        utils.slideTableStop()


def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    thread_UI.start()
