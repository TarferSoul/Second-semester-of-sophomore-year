import numpy as np
from functions import f1, g1, real_f1, real_g1, g2, f2, real_f2, real_g2, g3, real_g3, f3, real_f3

'''
第一题，用欧拉法解一阶常微分方程组的初值问题
'''
def euler_method(f, g, x0, y0, h, N):
    x = np.zeros(N + 1)
    y = np.zeros(N + 1)
    x[0], y[0] = x0, y0
    for i in range(N):
        x[i + 1] = x[i] + h * f(x[i], y[i])
        y[i + 1] = y[i] + h * g(x[i], y[i])
    return x, y


def euler_method_for_f3(f, g, x0, y0, h, N):
    x = np.zeros(N + 1)
    y = np.zeros(N + 1)
    x[0], y[0] = x0, y0
    t = 0
    for i in range(N):
        x[i + 1] = x[i] + h * f(x[i], y[i])
        y[i + 1] = y[i] + h * g(x[i], y[i], t + h * i)
    return x, y


def print_results(x, y, real_f, real_g, h):
    print(f"当h={h}时:\n")
    print("近似x:", ["{:.4f}".format(i) for i in x])
    print("真实x:", ["{:.4f}".format(real_f(i)) for i in np.arange(0, h * 4, h)])
    print("近似y:", ["{:.4f}".format(i) for i in y])
    print("真实y:", ["{:.4f}".format(real_g(i)) for i in np.arange(0, h * 4, h)])
    print("----------------\n")


print("第一个方程组:\n")
x1, y1 = euler_method(f1, g1, 1, 0, 0.25, 3)
print_results(x1, y1, real_f1, real_g1, 0.25)
x1_1, y1_1 = euler_method(f1, g1, 1, 0, 0.125, 3)
print_results(x1_1, y1_1, real_f1, real_g1, 0.125)

print("第二个方程组:\n")
x2, y2 = euler_method(f2, g2, 5, 4, 0.25, 3)
print_results(x2, y2, real_f2, real_g2, 0.25)
x2_1, y2_1 = euler_method(f2, g2, 5, 4, 0.125, 3)
print_results(x2_1, y2_1, real_f2, real_g2, 0.125)

print("第三个方程组:\n")
x3, y3 = euler_method_for_f3(f3, g3, 0, 2, 0.25, 3)
print_results(x3, y3, real_f3, real_g3, 0.25)
x3_1, y3_1 = euler_method_for_f3(f3, g3, 0, 2, 0.125, 3)
print_results(x3, y3, real_f3, real_g3, 0.125)