from functions import B, T
from problem1 import euler_method, print_results
import matplotlib.pyplot as plt
import numpy as np
'''
第二题，估计两种鱼类的数量,图片见同一目录下
'''

B, T = euler_method(B, T, 5, 2, 0.1, 70)
print("近似x:", ["{:.4f}".format(i) for i in B])
print("近似y:", ["{:.4f}".format(i) for i in T])

plt.figure(figsize=(14, 8), dpi=200)
plt.plot(np.arange(70 + 1) / 10, B, label='B')
plt.plot(np.arange(70 + 1) / 10, T, label='T')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.title('B and T')
plt.show()

plt.figure(figsize=(8, 6),dpi=200)
plt.plot(B, T, label='Phase Trajectory', color='b')
plt.scatter(B[0], T[0], color='r', label='Initial Point')
plt.xlabel('B')
plt.ylabel('T')
plt.legend()
plt.grid(True)
plt.title('Phase Space Trajectory')
plt.show()