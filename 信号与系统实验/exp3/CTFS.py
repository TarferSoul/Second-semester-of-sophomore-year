import numpy as np
import matplotlib.pyplot as plt


def CTFS(f, N, T, coefficient):
    K1 = -coefficient
    K2 = coefficient
    F_k = np.arange(K1, K2 + 1)
    a_k = np.arange(0, K2 + 1)
    b_k = a_k
    w1 = 2 * np.pi / T
    t = np.linspace(-T / 2, T / 2, N)

    exp_mat = np.zeros((K2 - K1 + 1, N), dtype=np.complex128)
    for k in range(K1, K2 + 1):
        for n in range(N):
            exp_mat[k - K1, n] = np.exp(-1j * (k) * t[n] * w1)

    f_mat = np.transpose([f])
    FS = 1 / N * np.dot(np.transpose(exp_mat), f_mat)

    a = np.zeros(((K2 - K1) // 2 + 1,), dtype=np.complex128)
    b = np.zeros(((K2 - K1) // 2 + 1,), dtype=np.complex128)
    for p in range(0, (K2 - K1) // 2 + 1):
        a[0] = FS[(K2 - K1) // 2, 0]
        a[p + 1] = FS[(K2 - K1) // 2 - p, 0] + FS[(K2 - K1) // 2 + p, 0]
        b[0] = 0
        b[p + 1] = 1j * (FS[(K2 - K1) // 2 + p, 0] - FS[(K2 - K1) // 2 - p, 0])

    i_exp_mat = np.zeros((N, K2 + 1))
    for k in range(N):
        for n in range(K2 + 1):
            i_exp_mat[k, n] = np.cos((n) * w1 * t[k])

    i_f = np.dot(i_exp_mat, np.transpose([a]))

    return FS


# Example usage
N = 500
T = 1
t = np.linspace(-T / 2, T / 2, N)
f = np.sinc(t)
coefficient = 10
ctfs = CTFS(f, N, T, coefficient)

# Plotting
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(t, f)
plt.title('Original Signal')
plt.subplot(2, 2, 2)
plt.stem(np.arange(-coefficient, coefficient + 1), np.abs(ctfs))
plt.title('Magnitude of FS(k)')
plt.subplot(2, 2, 3)
plt.stem(np.arange(0, coefficient + 1), np.abs(a))
plt.title('Magnitude of a(k)')
plt.subplot(2, 2, 4)
plt.stem(np.arange(0, coefficient + 1), np.abs(b))
plt.title('Magnitude of b(k)')
plt.tight_layout()
plt.show()
