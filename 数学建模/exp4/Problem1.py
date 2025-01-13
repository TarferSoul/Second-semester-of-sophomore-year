import pulp
from pulp import PULP_CBC_CMD
WaterSupply = pulp.LpProblem('Problem1', sense=pulp.LpMaximize)

# 决策变量
# x1 = pulp.LpVariable('x1', lowBound=0, upBound=50, cat='Continuous')  # A->甲
# x2 = pulp.LpVariable('x2', lowBound=0, upBound=50, cat='Continuous')  # A->乙
# x3 = pulp.LpVariable('x3', lowBound=0, upBound=50, cat='Continuous')  # A->丙
# x4 = pulp.LpVariable('x4', lowBound=0, upBound=50, cat='Continuous')  # A->丁

# y1 = pulp.LpVariable('y1', lowBound=0, upBound=60, cat='Continuous')  # B->甲
# y2 = pulp.LpVariable('y2', lowBound=0, upBound=60, cat='Continuous')  # B->乙
# y3 = pulp.LpVariable('y3', lowBound=0, upBound=60, cat='Continuous')  # B->丙
# y4 = pulp.LpVariable('y4', lowBound=0, upBound=60, cat='Continuous')  # B->丁

# z1 = pulp.LpVariable('z1', lowBound=0, upBound=50, cat='Continuous')  # C->甲
# z2 = pulp.LpVariable('z2', lowBound=0, upBound=50, cat='Continuous')  # C->乙
# z3 = pulp.LpVariable('z3', lowBound=0, upBound=50, cat='Continuous')  # C->丙

# 决策变量 水库供水量提高一倍
x1 = pulp.LpVariable('x1', lowBound=0, upBound=100, cat='Continuous')  # A->甲
x2 = pulp.LpVariable('x2', lowBound=0, upBound=100, cat='Continuous')  # A->乙
x3 = pulp.LpVariable('x3', lowBound=0, upBound=100, cat='Continuous')  # A->丙
x4 = pulp.LpVariable('x4', lowBound=0, upBound=100, cat='Continuous')  # A->丁

y1 = pulp.LpVariable('y1', lowBound=0, upBound=120, cat='Continuous')  # B->甲
y2 = pulp.LpVariable('y2', lowBound=0, upBound=120, cat='Continuous')  # B->乙
y3 = pulp.LpVariable('y3', lowBound=0, upBound=120, cat='Continuous')  # B->丙
y4 = pulp.LpVariable('y4', lowBound=0, upBound=120, cat='Continuous')  # B->丁

z1 = pulp.LpVariable('z1', lowBound=0, upBound=100, cat='Continuous')  # C->甲
z2 = pulp.LpVariable('z2', lowBound=0, upBound=100, cat='Continuous')  # C->乙
z3 = pulp.LpVariable('z3', lowBound=0, upBound=100, cat='Continuous')  # C->丙

# 目标函数
WaterSupply += 450 * (x1 + x2 + x3 + x4 + y1 + y2 + y3 + y4 + z1 + z2 + z3) - \
               (160 * x1 + 130 * x2 + 220 * x3 + 170 * x4) - \
               (140 * y1 + 130 * y2 + 190 * y3 + 150 * y4) - \
               (190 * z1 + 200 * z2 + 230 * z3)

# 水库供水量约束条件
# WaterSupply += (x1 + x2 + x3 + x4 <= 50)
# WaterSupply += (y1 + y2 + y3 + y4 <= 60)
# WaterSupply += (z1 + z2 + z3 <= 50)

# 水库供水量约束条件 提高一倍
WaterSupply += (x1 + x2 + x3 + x4 <= 100)
WaterSupply += (y1 + y2 + y3 + y4 <= 120)
WaterSupply += (z1 + z2 + z3 <= 100)

# 小区需求用水约束条件
WaterSupply += (x1 + y1 + z1 >= 30)
WaterSupply += (x1 + y1 + z1 <= 80)
WaterSupply += (x2 + y2 + z2 >= 70)
WaterSupply += (x2 + y2 + z2 <= 140)
WaterSupply += (x3 + y3 + z3 >= 10)
WaterSupply += (x3 + y3 + z3 <= 30)
WaterSupply += (x4 + y4 >= 10)
WaterSupply += (x4 + y4 <= 50)

WaterSupply.solve(PULP_CBC_CMD(msg=False))
print('Status:', pulp.LpStatus[WaterSupply.status])
for v in WaterSupply.variables():
    print(v.name, '=', v.varValue)
print("F(x)= ", pulp.value(WaterSupply.objective))
