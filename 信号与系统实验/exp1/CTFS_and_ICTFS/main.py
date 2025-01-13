import numpy as np
import matplotlib.pyplot as plt

E = 1
T1 = 1
N = 100

def f(t):
    if abs(t) <= T1 / 4:
        return E / 2
    elif T1 / 4 <= abs(t) <= T1 / 2:
        return -E / 2
    else:
        return 0


def CTFS(N):
    x_values = np.linspace(-0.5, 0.5, N)
    x = np.array([f(t) for t in x_values])
    x_matrix = x.reshape(-1, 1)

    rows, cols = N, N
    matrix = np.zeros((rows, cols), dtype=complex)

    # 填充矩阵元素
    for i in range(rows):
        for j in range(cols):
            k1 = -10
            w1 = 2 * np.pi
            t0 = -0.5
            delta_t = 1 / N

            # 计算矩阵元素
            element = np.exp(-1j * ((k1 + i) * w1 * (t0 + j * delta_t)))
            matrix[i, j] = element

    y_matrix = np.zeros((1, N)).reshape(-1, 1)
    y_matrix = np.dot(matrix, x_matrix) * (1 / N)
    return y_matrix


def ICTFS(N, y):
    rows, cols = N, N
    matrix = np.zeros((rows, cols), dtype=complex)

    # 填充矩阵元素
    for i in range(rows):
        for j in range(cols):
            k1 = -10
            w1 = 2 * np.pi
            t0 = -0.5
            delta_t = 1 / N

            # 计算矩阵元素
            element = np.exp(1j * ((k1 + i) * w1 * (t0 + j * delta_t)))
            matrix[i, j] = element

    z = np.dot(matrix, y)
    return z


if __name__ == '__main__':
    F = CTFS(N)
    ft = ICTFS(N, F)
    print(F)

    a_0 = F[0]
    a_k = [F[K] + F[-K] for K in range(0, 11)]
    plt.stem(range(0, 11), a_k, use_line_collection=True)
    plt.xlabel('k')
    plt.ylabel('|a_k|')
    plt.title('a_k vs. k')
    plt.show()

