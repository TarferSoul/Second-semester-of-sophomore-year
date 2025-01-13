from scipy.optimize import minimize, Bounds
import math
import numpy as np

weight_ini = 800
weight_put_on_per_week = 35
price_per_pound_ini = 0.95
price_decrease_per_week = 0.01
cost_per_week = 6.5


def profit(n):
    return -((weight_ini + weight_put_on_per_week * n) *
             (price_per_pound_ini - price_decrease_per_week * n) - cost_per_week * n)


n_ini = np.array([0])
bounds = Bounds([0], [np.inf])
p_max = minimize(profit, n_ini, bounds=bounds)

if profit(int(p_max.x[0])) >= profit(math.ceil(p_max.x[0])):
    print(f"在第", math.ceil(p_max.x[0]), '周卖出,最大利润为%.2f' % -profit(int(p_max.x[0])))
else:
    print(f"在第", int(p_max.x[0]), '周卖出,最大利润为%.2f' % -profit(math.ceil(p_max.x[0])))
