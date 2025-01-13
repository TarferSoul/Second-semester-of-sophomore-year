from scipy.optimize import minimize, Bounds
import numpy as np

e = 1e-7


def func(x):
    return -(18 * x[0] + 2 * x[1] - 0.05 * (x[0] ** 2) - 0.03 * (x[1] ** 2) + 0.02 * x[0] * x[1] - 100)


x_ini = np.array([1, 1])
bounds = Bounds([0, 0], [np.inf, np.inf])
p_max = minimize(func, x_ini, bounds=bounds)

print(f"x=", p_max.x[0], f"y=", p_max.x[1])
print(f"最大利润:", -p_max.fun)
