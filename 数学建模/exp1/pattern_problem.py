def coordinates_cal(p): # 计算坐标
    if p < 1 or p > 9:
        raise ValueError("Invalid input")

    x = (p - 1) % 3 + 1
    y = (p - 1) // 3 + 1

    return x, y


def is_valid_move(p1, p2, pattern):  # 判断移动是否有效
    if p1 in (1, 3, 7, 9) and p2 in (1, 3, 7, 9) and (p1 + p2) / 2 in pattern:
        return False
    if p1 + p2 == 10 and 5 in pattern:
        return False
    if p2 in pattern or p1 == p2:
        return False
    x1, y1 = coordinates_cal(p1)
    x2, y2 = coordinates_cal(p2)

    for i in range(1, len(pattern)):
        px1, py1 = coordinates_cal(pattern[i - 1])
        px2, py2 = coordinates_cal(pattern[i])
        if (px2 != px1) and (x2 != x1) and ((py2 - py1) / (px2 - px1) == (y2 - y1) / (x2 - x1)):
            return False
        if (px2 == px1) and (x2 == x1):
            return False
    return True


def dfs(pattern, length, result, visited):  # dfs遍历
    if length == 0:
        result.append(pattern[:])
        return
    for i in range(1, 10):
        if not visited[i] and (not pattern or is_valid_move(pattern[-1], i, pattern)):
            pattern.append(i)
            visited[i] = True
            dfs(pattern, length - 1, result, visited)
            pattern.pop()
            visited[i] = False


def generate_patterns():  # 生成图案
    result = []
    visited = [False] * 10

    dfs([], 8, result, visited)
    return result


def save_files(patterns):  # 保存文件
    with open("patterns.txt", "w") as f:
        for pattern in patterns:
            f.write(" ".join(map(str, pattern)) + "\n")


if __name__ == "__main__":
    patterns = generate_patterns()
    save_files(patterns)
