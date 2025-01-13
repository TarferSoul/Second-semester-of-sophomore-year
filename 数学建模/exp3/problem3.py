import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds


def yearly_cost_function(t):
    return 640 + 180 * (t + 1) * t


def total_cost_function(t):
    return 9000 + yearly_cost_function(t)


def average_cost_function(t):
    return total_cost_function(t) / t


t = np.linspace(1, 20, 100)
plt.plot(t, average_cost_function(t), label='E_a(t)')
plt.xlabel('t')
plt.ylabel('E_a(t)')
plt.title('Average Cost Function Over Time')
plt.legend()
plt.show()

t_ini = np.array([0.1])
bounds = Bounds([0.1], [np.inf])
total_time = minimize(average_cost_function, t_ini)
print('最佳报废年限为:', f"%.2f" % total_time.x[0], '年,总成本为:', f"%.2f" % total_time.fun, '元')
