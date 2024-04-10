from collections import deque
from itertools import permutations

def can_move(map, row, col):
    return (row >= 0) and (row < len(map)) and \
    (col >= 0) and (col < len(map[0])) and \
    (map[row][col] == 0)

def bfs_level1(map, start, goal):
    visited = [[False] * len(map[0]) for i in range(len(map))]

    steps = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # up, down, left, right, north-west, north-east, south-west, south-east

    queue = deque([(start[0], start[1], 0, [])]) #(row, col, cost, path)
    visited[start[0]][start[1]] = True

    while len(queue) > 0:
        row, col, cost, path = queue.popleft()
        for row_step, col_step in steps:
            next_row = row + row_step
            next_col = col + col_step
            if not visited[next_row][next_col]:
                if can_move(map, next_row, next_col):
                    cost += 1
                    newPath = path + [(row, col)]
                    if next_row == goal[0] and next_col == goal[1]:
                        newPath.append((next_row, next_col))
                        return (cost, newPath)
                    else:
                        queue.append((next_row, next_col, cost, newPath))
                        visited[next_row][next_col] = True

    return None


def bfs_level3(map, start, goal, must_passes):
    # must_passes là mảng gồm một tập các điểm đón phải đi qua
    # giả sử ta ký hiệu luôn đại diện cua mỗi điểm đón là vị trí của điểm đó trong mảng must_passes

    d = [['inf'] * len(must_passes) for i in range(len(must_passes))] # khởi tạo khoảng cách giữa các điểm đến là vô cùng
    sz = len(must_passes) # so diem don phai di qua

    for m in range(len(must_passes)):
        for n in range(len(must_passes)):
            d[m][n] = bfs_level1(map.copy(), must_passes[m], must_passes[n])

    shortest = float('inf')
    shortest_path = []
    for permutation in permutations(range(sz)):
        gap = 0
        new_path = []
        res = bfs_level1(map.copy(), start, must_passes[permutation[0]])
        gap += res[0] #khoảng cách giữa start và điểm đón đầu tiên
        new_path += res[1]
        for i in range(len(must_passes) - 1):
            distance = d[permutation[i]][permutation[i + 1]] #khoảng cách giữa các điểm đón
            gap += distance[0]
            new_path += d[permutation[i]][permutation[i + 1]][1][1:]
        res = bfs_level1(map.copy(), must_passes[permutation[sz - 1]], goal)
        gap += res[0] # khoảng cách giữa điểm đón cuối cùng và goal
        new_path += res[1][1:]

        if(gap < shortest):
            shortest = gap
            shortest_path = new_path

    return (shortest, shortest_path)



map = [
    ['#','#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 0, 0, 0, 0, 0, 0, 0, 0, '#'],
    ['#', 0, '#', '#', '#', 0, '#', '#', 0, '#'],
    ['#', 0, 0, 0, '#', 0, 0, 0, 0, '#'],
    ['#', 0, '#', 0, 0, 0, '#', '#', 0, '#'],
    ['#', 0, '#', '#', '#', '#', '#', 0, 0, '#'],
    ['#', 0, 0, 0, 0, 0, 0, 0, 0, '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

must_passes = [(3, 1), (4, 4), (6, 6)]

start = (1, 1)
goal = (6, 8)

# cost, path = bfs_level1(map, start, goal)

cost, path = bfs_level3(map.copy(), start, goal, must_passes)

print(cost, path)
