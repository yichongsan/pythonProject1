import binascii, threading
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from math import factorial
from PyQt5.QtWidgets import QMessageBox
from scipy import signal
import UI

# 初始化全局变量
com = 0  # 点击开启串口次数
result_list = []  # 深度数据
time_list = []  # 时间数据
N = 0  # 传感器测量次数
avg = 0  # 深度平均值
begin = 1  # 开始测量
time_now = 0  # 目前的测量时间点
time_dis = 0  # 传感器测量轮胎这个过程所经历的时间
num_stop = 0  # 传感器测量不到数据的次数(经过轮胎之后)
STOP = process_data_done = False  # 传感器测量结束；处理数据结束
file_distance = open('distance.txt', mode='w')
file_time = open('time.txt', mode='w')
peak = []
px = py = []
dis = 0
END = False  # 整体计算结束
global ser, ser1


class thread_init(threading.Thread):
    def run(self):
        init()


thread_init = thread_init()


def init():
    global com, result_list, time_list, N, avg, begin, time_now, \
        time_dis, num_stop, STOP, process_data_done, file_distance, file_time, peak, px, py, dis, END, ser, ser1
    # 初始化全局变量
    com = 0  # 点击开启串口次数
    result_list = []  # 深度数据
    time_list = []  # 时间数据
    N = 0  # 传感器测量次数
    avg = 0  # 深度平均值
    begin = 1  # 开始测量
    time_now = 0  # 目前的测量时间点
    time_dis = 0  # 传感器测量轮胎这个过程所经历的时间
    num_stop = 0  # 传感器测量不到数据的次数(经过轮胎之后)
    STOP = process_data_done = False  # 传感器测量结束；处理数据结束
    file_distance = open('distance.txt', mode='w')
    file_time = open('time.txt', mode='w')
    peak = []
    px = py = []
    dis = 0
    END = False  # 整体计算结束


# 打开并连接串口


def openCom():
    global ser
    global ser1
    try:
        ser = serial.Serial('COM5', 9600, timeout=0.5)
        ser1 = serial.Serial('COM7', 9600, timeout=0.5, parity='E', bytesize=7, stopbits=1)
    except Exception as e:
        print(e)
        return False

    if ser.isOpen() and ser1.isOpen():
        print("Open Successful")
        return True


def slideTableRun():
    global ser1
    code = b'\x02\x37\x30\x30\x30\x34\x03\x46\x45'
    ser1.write(code)


def slideTableStop():
    global ser1
    code = b'\x02\x37\x30\x31\x30\x34\x03\x46\x46'
    ser1.write(code)


class thread_openSlide(threading.Thread):
    def run(self):
        openSlide()


thread_openSlide = thread_openSlide()  # 初始化开启电机、初始化脉冲数线程


# 开启电机、初始化脉冲数
def openSlide():
    global ser
    global ser1
    # 按钮x4复位(清零)D8140寄存器
    restore_pulse = b'\x02\x37\x30\x34\x30\x34\x03\x30\x32'
    ser1.write(restore_pulse)

    time.sleep(0.1)
    # 启动丝杆滑台电机
    code = b'\x02\x37\x30\x30\x30\x34\x03\x46\x45'
    ser1.write(code)
    global time_slide_begin
    time_slide_begin = time.time()


class thread_pulse_Width(threading.Thread):
    def run(self):
        pulse_Width()


thread_pulse_Width = thread_pulse_Width()  # 初始化计算脉冲和轮胎宽度线程


# 计算脉冲和轮胎宽度
def pulse_Width():
    global result_list, time_list, N, avg, begin, time_now, \
        num_stop, STOP, file_distance, file_time, time_dis, ser, ser1
    # 测量结束，读取D8140寄存器存储值
    if STOP:
        time_sensor_stop = time.time()
        ser1.close()
        ser1 = serial.Serial('COM7', 9600, timeout=0.5, parity='E', bytesize=7, stopbits=1)
        # 将time_list转化为长度单位
        pulse_code = b'\x02\x30\x30\x46\x31\x38\x30\x32\x03\x37\x34'
        ser1.write(pulse_code)
        time.sleep(0.1)
        count = ser1.inWaiting()
        run_distance = 0
        if count > 0:
            data = ser1.read(count)
            if data != b'':
                a = str(binascii.b2a_hex(data))[4:-3]
                a = a.encode('utf-8')
                a = binascii.a2b_hex(a).decode()
                a = a[0:4]
                print(a)
                b = a[2:4] + a[0:2]
                b = int(b, 16)  # 输入16进制的数并转换成10进制
                run_distance = b * 0.05
                time_through_all = time_sensor_stop - time_slide_begin
                run_distance = run_distance * (time_dis / time_through_all)
        ser1.close()
        for i in range(len(time_list)):
            time_list[i] = (time_list[i] * run_distance) / time_dis


class thread_Measure(threading.Thread):
    def run(self):
        measure()


thread_Measure = thread_Measure()  # 初始化测量深度数据线程


# 测量深度数据
def measure():
    global result_list, time_list, N, avg, begin, time_now, \
        num_stop, STOP, file_distance, file_time, time_dis, ser, ser1

    measure_255 = b'\x02\x4d\x45\x41\x53\x55\x52\x45\x20\x32\x35\x35\x03'
    ser.write(measure_255)
    time.sleep(0.05)
    count = ser.inWaiting()
    if count == 0 and N == 0:
        print("正在等待测量")
        time_now = time.time()  # 持续更新，直到开始测量
    if count > 0:
        data = ser.read(count)
        if data != b'':
            a = str(binascii.b2a_hex(data))[4:-3]
            a = a.encode('utf-8')
            a = binascii.a2b_hex(a).decode()
            if '?' in a:
                return None
            b = str(a)[0:6]
            b = float(b)
            # 离群点检测
            if N > 0:
                if abs(b - result_list[N - 1]) > 10:
                    return None
            avg += b
            result_list.append(b)
            b = str(b)
            print(b + "mm")
            time_list.append(time.time() - time_now)
            file_distance.write(b + '\n')
            file_time.write(str(time_list[N]) + '\n')
            N += 1
            return float(b)

    if count == 0 and N != 0:  # 判断是否已经测量结束
        measure_255 = b'\x02\x4d\x45\x41\x53\x55\x52\x45\x20\x32\x35\x35\x03'
        ser.write(measure_255)
        time.sleep(0.05)
        count1 = ser.inWaiting()
        if count1 == 0:
            num_stop += 1
    if num_stop == 3:
        avg = avg / N
        time_end = time.time()  # 传感器测量不到轮胎花纹的时间点(结束测量的时候)
        time_dis = time_end - time_now
        print("测量结束,本次测量次数：" + str(N) + "\n" + "本次测量平均深度:" + str(avg) + "\n" + "本次测量所用时间：" + str(time_dis))
        ser.close()  # 激光位移传感器结束测量
        begin = 0
        STOP = True


class thread_process_Data(threading.Thread):
    def run(self):
        processData()


thread_process_Data = thread_process_Data()  # 初始化数据处理线程


# 对数据进行处理
def processData():
    global result_list, time_list, peak, px, py, process_data_done
    print("正在处理数据")
    # 对测量数据进行插值(增多一倍)
    lens = len(result_list)
    for i in range(len(result_list)):
        if i == lens - 1:
            break
        else:
            result_list.insert(2 * i + 1, (result_list[2 * i] + result_list[2 * i + 1]) / 2)
            time_list.insert(2 * i + 1, (time_list[2 * i] + time_list[2 * i + 1]) / 2)

    # 将数据转换为实际中的样子
    for i in range(len(result_list)):
        result_list[i] = 2 * avg - result_list[i]
    # 对数据进行拟合，并寻找极大值点
    lens = len(result_list)
    n = lens - 1
    px = []
    py = []
    for T in range(200):
        t = T / 200
        x1, y1 = 0, 0
        for i in range(lens):
            if i == t == 0:
                B = 1
            else:
                B = (Decimal(factorial(n)) * Decimal(t) ** Decimal(i) * Decimal(1 - t) ** Decimal(n - i)) / (
                        Decimal(factorial(i)) * Decimal(factorial(n - i)))
            x1 += Decimal(time_list[i]) * B
            y1 += Decimal(result_list[i]) * B

        px.append(x1)
        py.append(y1)
    py = np.array(py)
    peak = signal.find_peaks(py)
    # 检查第一个和最后一个凹槽，判断并找出不属于轮胎花纹的凹槽，并将他去除；判断条件：1.极值点之间相差过大；2.极小值点附近点数过多，同时满足以上两个条件判断此凹槽不属于轮胎花纹凹槽
    if abs(result_list[peak[0][0]] - result_list[peak[0][1]]) > 3:
        del (peak[0][0])
    if abs(result_list[peak[0][-1]] - result_list[peak[0][-2]]) > 3:
        del (peak[0][-1])
    for i in range(len(peak[0])):
        peak[0][i] = peak[0][i] * lens / 200
    print(peak)
    process_data_done = True


class thread_caculate_Depth(threading.Thread):
    def run(self):
        caculateDepth()


thread_caculate_Depth = thread_caculate_Depth()  # 初始化计算深度线程


# 计算深度值，生成单个和总体的轮胎图片
def caculateDepth():
    global peak, dis, END
    file = open("result.txt", mode='w')  # 保存每个花纹深度结果
    # 判断并找出不属于轮胎花纹的凹槽，并将他去除；判断条件：1.极值点之间相差过大；2.极小值点附近点数过多，同时满足以上两个条件判断此凹槽不属于轮胎花纹凹槽
    # 1.显示保存每个轮胎花纹图案；2.找到每个胎面的最小值；3.找到当前花纹所有点都在其下方的切线，并求出与胎面最小值的垂直距离
    for i in range(len(peak[0]) - 1):
        # 1.显示保存每个轮胎花纹图案
        plt.plot(time_list[peak[0][i]:peak[0][i + 1]], result_list[peak[0][i]:peak[0][i + 1]])
        plt.ylabel('Contour Line/mm')
        plt.xlabel('Tire Width/s')
        plt.ylim(avg - 10, avg + 10)
        plt.title("tread" + str(i + 1))
        plt.savefig("tread" + str(i + 1) + ".png")
        plt.close()
        # 2.找到每个胎面的最小值
        tmp = result_list[peak[0][i]]
        minNum = 0
        for j in range(peak[0][i], peak[0][i + 1]):
            if result_list[j] < tmp:
                tmp = result_list[j]
                minNum = j
        # 3.找到当前花纹所有点都在其下方的切线，并求出与胎面最小值的垂直距离
        # 3.1找到最低点和两边极值点之间的最大值
        x1 = x2 = 0
        for l in range(peak[0][i], minNum):
            if result_list[l] > result_list[x1]:
                x1 = l
        for r in range(minNum, peak[0][i + 1]):
            if result_list[r] > result_list[x2]:
                x2 = r
        print(x1, x2)
        # 3.2最小值两边的最大值已经找到，开始寻找切线
        a = result_list[x2] - result_list[x1]
        b = time_list[x1] - time_list[x2]
        c = result_list[x1] * (time_list[x2] - time_list[x1]) - time_list[x1] * (result_list[x2] - result_list[x1])
        # 3.3求最小值两边大于该切线的点，并更新切线
        disL = disR = numL = numR = 0
        for l in range(peak[0][i], minNum):
            verDis = abs(a * time_list[l] + b * result_list[l] + c) / ((a ** 2 + b ** 2) ** 0.5)
            y = -(a / b) * time_list[l] - (c / b)
            if verDis > disL and y < result_list[l]:
                disL = verDis
                numL = l
        if numL == 0:
            numL = x1
        for r in range(minNum, peak[0][i + 1]):
            verDis = abs(a * time_list[r] + b * result_list[r] + c) / ((a ** 2 + b ** 2) ** 0.5)
            y = -(a / b) * time_list[r] - (c / b)
            if verDis > disR and y < result_list[r]:
                disR = verDis
                numR = r
        if numR == 0:
            numR = x2
        print(numL, minNum, numR)
        # 3.4更新直线参数
        a = result_list[numR] - result_list[numL]
        b = time_list[numL] - time_list[numR]
        c = result_list[numL] * (time_list[numR] - time_list[numL]) - time_list[numL] * (
                result_list[numR] - result_list[numL])
        # 3.5直线已经更新完，现在开始进行计算最小值点和直线的垂直距离
        if a == b == 0:
            continue
        # dis = abs(a * time_list[minNum] + b * result_list[minNum] + c) / ((a ** 2 + b ** 2) ** 0.5)
        dis = -(a / b) * time_list[minNum] - (c / b) - result_list[minNum]
        if dis < 3:
            continue
        print("第" + str(i + 1) + "个轮胎花纹深度为：" + str(round(dis, 4)) + "mm")

        file.write(str(dis) + '\n')
        # Ui_MainWindow.printf(self, "第" + str(i + 1) + "个轮胎花纹深度为：" + str(round(dis, 4)) + "mm")

    plt.plot(time_list, result_list, label='original values')
    plt.plot(px, py, 'r', label='polyfit values')
    plt.legend(loc=4)
    plt.ylabel('Contour Line/mm')
    plt.xlabel('Tire Width/mm')
    plt.ylim(40, 115)
    plt.savefig("treadAll.png")

    for i in range(len(peak[0])):
        plt.plot(time_list[peak[0][i]], result_list[peak[0][i]], '*', markersize=10)

    plt.show()
    END = True


if __name__ == '__main__':
    openCom()
    openSlide()
