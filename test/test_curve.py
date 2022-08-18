from decimal import Decimal
from math import factorial
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

result_list = np.loadtxt('E:\Python File\RS485\data\data.txt')
time_list = np.loadtxt('E:\Python File\RS485\data/time.txt')

N = len(result_list)
avg = max = 0
min = 105
for i in range(N):
    if result_list[i] > max:
        max = result_list[i]
    if result_list[i] < min:
        min = result_list[i]
    avg += result_list[i]
dis = max - min
avg = avg / N
for i in range(N):
    result_list[i] = 2 * avg - result_list[i]

n = N - 1
px = []
py = []
for T in range(100):
    t = T / 100
    x1, y1 = 0, 0
    for i in range(N):
        if i == t == 0:
            B = 1
        else:
            B = ((factorial(n)) * t ** i * (1 - t) ** (n - i)) / (
                    (factorial(i)) * (factorial(n - i)))
        a = (result_list[i] - avg) / avg
        if result_list[i] > (avg + 3):
            x1 += (time_list[i]) * B
            y1 += (result_list[i]) * B * (1 + 2 * a)
        elif result_list[i] < (avg - 3):
            x1 += (time_list[i]) * B
            y1 += (result_list[i]) * B * 2 * a
        else:
            x1 += (time_list[i]) * B
            y1 += (result_list[i]) * B
    px.append(x1)
    py.append(y1)
py = np.array(py)
peak = signal.find_peaks(py)
for i in range(len(peak[0])):
    peak[0][i] = peak[0][i] * N / 100
print(peak)
# for ii in range(len(peak[0])):
#     plt.plot(time_list[peak[0][ii]], result_list[peak[0][ii]], '*', markersize=10)
# plt.plot(time_list, result_list)
# plt.plot(px, py)
# plt.show()

test_x = []
test_y = []
test_x.append(time_list[0])
test_y.append(result_list[0])
for i in range(len(peak[0]) - 1):
    test_x.append(time_list[peak[0][i]])
    test_y.append(result_list[peak[0][i]])
    min = 105
    min_j = 0
    for j in range(peak[0][i], peak[0][i + 1]):
        if result_list[j] < min:
            min = result_list[j]
            min_j = j
    test_x.append(time_list[min_j])
    test_y.append(min)
test_x.append(time_list[-1])
test_y.append(result_list[-1])
print(test_x)
print(test_y)
plt.plot(test_x, test_y)
avg = 0
for i in range(len(test_y)):
    avg += test_y[i]
avg = avg / len(test_y)
n = len(test_x) - 1
px = []
py = []
for T in range(10):
    t = T / 10
    x1, y1 = 0, 0
    for i in range(n + 1):
        if i == t == 0:
            B = 1
        else:
            B = ((factorial(n)) * t ** i * (1 - t) ** (n - i)) / (
                    (factorial(i)) * (factorial(n - i)))
        a = (test_y[i] - avg) / avg
        if test_y[i] > (avg + 3):
            x1 += (test_x[i]) * B
            y1 += (test_y[i]) * B * (1 + 2 * a)
        elif test_y[i] < (avg - 3):
            x1 += (test_x[i]) * B
            y1 += (test_y[i]) * B * (1 - 2 * a)
        else:
            x1 += (test_x[i]) * B
            y1 += (test_y[i]) * B
    px.append(x1)
    py.append(y1)
py = np.array(py)
peak = signal.find_peaks(py)
plt.plot(px, py)
plt.show()
