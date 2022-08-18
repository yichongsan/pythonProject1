import sys
import traceback
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import time
import numpy as np
import UI
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

import utils


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("轮胎花纹测量实时显示")
        self.main_widget = QtWidgets.QWidget()  # 创建一个主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建一个网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置主部件的布局为网格
        self.setCentralWidget(self.main_widget)  # 设置窗口默认部件

        self.plot_widget = QtWidgets.QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout = QtWidgets.QGridLayout()  # 实例化一个网格布局层
        self.plot_widget.setLayout(self.plot_layout)  # 设置K线图部件的布局层
        self.plot_plt = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout.addWidget(self.plot_plt)  # 添加绘图部件到K线图部件的网格布局层
        # 将上述部件添加到布局层中
        self.main_layout.addWidget(self.plot_widget, 1, 0, 3, 3)

        self.setCentralWidget(self.main_widget)
        self.plot_plt.setYRange(max=105, min=0)
        self.plot_plt.setXRange(0, 400)
        self.data_list = []
        self.timer_start()

    # 启动定时器 时间间隔秒
    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_depth)
        self.timer.start(100)

    # 获取深度数据
    def get_depth(self):
        try:
            if utils.STOP:
                self.timer.stop()
                # utils.processData()
                QMessageBox.information(self, "标题", "正在进行数据计算",
                                        QMessageBox.Yes)
                utils.thread_pulse_Width.start()  # 通过计算发送脉冲数计算轮胎脉冲
                utils.thread_pulse_Width.join()
                utils.thread_process_Data.start()  # 数据处理、拟合曲线等工作
                utils.thread_process_Data.join()
                print("处理数据结束，开始计算深度")
                # utils.caculateDepth()
                utils.thread_caculate_Depth.start()
                utils.thread_caculate_Depth.join()
                UI.Ui_MainWindow.showResult()

            else:
                cpu = utils.measure()
                if cpu is not None:
                    cpu = float(cpu)
                    cpu = 170 - cpu
                    if utils.N > 400:
                        self.plot_plt.setXRange(0, utils.N)
                    if utils.N < 200:
                        self.plot_plt.setXRange(0, 200)
                    self.data_list.append(cpu)
                    print(cpu)
                    self.plot_plt.plot().setData(self.data_list, pen='g')
                    self.time = time.time()

        except Exception as e:
            print(traceback.print_exc())


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
