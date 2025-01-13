###########################
# 假设原油加工的过程中没有损耗，即1吨原油A和1吨原油B可加工成2吨汽油甲
###########################
import pulp
from pulp import PULP_CBC_CMD
import time

def Purchase_Oil(x, y):
    if 0 <= x + y <= 500:
        return 10000 * (x + y)
    elif x + y <= 1000:
        return 10000 * 500 + 8000 * (x + y - 500)
    elif x + y <= 1500:
        return 18000 * 500 + 6000 * (x + y - 1000)
    else:
        return


StartTime = time.time()
solutions = []
OilProblem = pulp.LpProblem('Problem2', sense=pulp.LpMaximize)

x1 = pulp.LpVariable('x1', lowBound=0, upBound=500, cat='Continuous')  # A->甲
x2 = pulp.LpVariable('x2', lowBound=0, upBound=1000, cat='Continuous')  # A->乙
y1 = pulp.LpVariable('y1', lowBound=0, upBound=1000, cat='Continuous')  # B->甲
y2 = pulp.LpVariable('y2', lowBound=0, upBound=1000, cat='Continuous')  # B->乙
z1 = pulp.LpVariable('z1', lowBound=0, upBound=1000, cat='Continuous')  # 购买A->甲
z2 = pulp.LpVariable('z2', lowBound=0, upBound=1500, cat='Continuous')  # 购买A->乙

for i in range(0, 1501):

    OilProblem.constraints.clear()  # 清除所有约束条件
    OilProblem.objective = 4800 * (x1 + y1 + z1) + 5600 * (x2 + y2 + z2) - Purchase_Oil(i, 0)

    OilProblem += (x1 + z1 >= y1)
    OilProblem += ((x2 + z2) / 0.6 >= y2 * 1 / 0.4)
    OilProblem += (z1 + z2 == i)
    OilProblem += (y1 + y2 <= 1000)
    OilProblem += (x1 + x2 <= 500)

    OilProblem.name = f'Problem_{i}'
    OilProblem.solve(PULP_CBC_CMD(msg=False))
    SolutionList = []
    SolutionList.append(pulp.LpStatus[OilProblem.status])
    for v in OilProblem.variables():
        SolutionList.append(v.varValue)
    SolutionList.append(pulp.value(OilProblem.objective))
    print(i, SolutionList)
    solutions.append(SolutionList)

MaxProfit = max(solutions, key=lambda x: x[-1])
print(MaxProfit)
EndTime = time.time()
print('运行时间:', EndTime - StartTime, 's')
