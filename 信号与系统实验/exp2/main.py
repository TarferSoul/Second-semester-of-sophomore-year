import numpy as np
import matplotlib.pyplot as plt


# 定义函数 f(t)
def f(t, tau, epsilon=1):
    return np.where(np.abs(t) <= tau / 2, 1 - 2 * np.abs(t), 0)


tau = 1
epsilon = 1

fs = 1000
t = np.linspace(-1, 1, fs, endpoint=True)

f1 = np.zeros(fs)
for i in range(fs):
    f1[i] = f(t[i], tau, epsilon)

F = np.fft.fft(f1)
freqs = np.fft.fftfreq(len(t), t[1]-t[0])
plt.plot(freqs, 2.0/len(t)*np.abs(F))
plt.xlim(-50, 50)
# plt.figure(figsize=(8,6),dpi=200)
# plt.plot(t, f1, label='f(t)')
plt.show()