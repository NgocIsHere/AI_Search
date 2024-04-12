import pygame
import random
import math
import time
import sys
from pygame.locals import *
import heapq
from collections import deque


pygame.init()
width = 1280
height = 700
clock = pygame.time.Clock()
FPS = 60
column = 7
row = 4

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

ifrom, ito, jfrom, jto = 0, 0, 0, 0
width_rec = 45
# Define the directions: Up, Down, Left, Right
# directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

pygame.init()
clock = pygame.time.Clock()
width = 1280
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
              (1, 1), (-1, -1), (1, -1), (-1, 1)]


class Robot:
    def __init__(self):
        self.posi = 1
        self.posj = 0
        self.posx = 0
        self.posy = 0
        self.v = 3
        self.step = 0
        self.robot_image = pygame.transform.scale(pygame.image.load(
            "./image/robot.png"), (width_rec/2, width_rec/2))
        self.direction_queue = []

    def move(self):
        if len(self.direction_queue) != 0:
            self.posx += self.v * (self.direction_queue[0][1] - self.posj)
            self.posy += self.v * (self.direction_queue[0][0] - self.posi)
            self.step += self.v

        if self.step == width_rec:
            if (len(self.direction_queue) != 0):
                self.posj = self.direction_queue[0][1]
                self.posi = self.direction_queue[0][0]
                self.direction_queue.pop(0)
            self.posx = self.posy = 0
            self.step = 0
            return True
        return False


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_path_dfs(rows, cols, start, end, table):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1),
                  (1, -1), (1, 1)]  # Hướng di chuyển: phải, trái, xuống, lên

    # Khởi tạo stack chứa các ô cần kiểm tra
    stack = [start]

    # Khởi tạo bản đồ các ô đã được đi qua
    visited = set()
    visited.add(start)

    # Khởi tạo bản đồ đường đi từ start đến mỗi ô và ô cha của nó
    parent_map = {start: None}

    # Duyệt stack
    while stack:
        current = stack.pop()
        if current == end:
            break

        # Duyệt các ô lân cận
        for dx, dy in directions:
            new_cell = (current[0] + dx, current[1] + dy)
            if 0 <= new_cell[0] < rows and 0 <= new_cell[1] < cols and table[new_cell[0]][new_cell[1]] not in (1, 4) and new_cell not in visited:
                visited.add(new_cell)
                stack.append(new_cell)
                parent_map[new_cell] = current

    if end not in visited:
        return None  # Không tìm được đường đi
    # Tạo đường đi từ end đến start
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent_map[current]
    path.append(start)
    path.reverse()
    return path


def find_path_bfs(rows, cols, start_point, end_point, map):
    print(map)
    def can_move(map, row, col):
        return (row >= 0) and (row < len(map)) and \
            (col >= 0) and (col < len(map[0])) and \
            (map[row][col] != 1 and map[row][col] != 4)

    visited = [[False] * len(map[0]) for i in range(len(map))]

    # up, down, left, right, north-west, north-east, south-west, south-east
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1),
             (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # (row, col, cost, path)
    queue = deque([(start_point[0], start_point[1], 0, [])])
    visited[start_point[0]][start_point[1]] = True

    while len(queue) > 0:
        row, col, cost, path = queue.popleft()
        for row_step, col_step in steps:
            next_row = row + row_step
            next_col = col + col_step
            if not visited[next_row][next_col]:
                if can_move(map, next_row, next_col):
                    cost += 1
                    newPath = path + [(row, col)]
                    if next_row == end_point[0] and next_col == end_point[1]:
                        newPath.append((next_row, next_col))
                        return newPath
                    else:
                        queue.append((next_row, next_col, cost, newPath))
                        visited[next_row][next_col] = True

    return None


def find_path_greedy(rows, cols, start, end, table):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1),
                  (1, -1), (1, 1)]  # Hướng di chuyển: phải, trái, xuống, lên

    # Hàm tính khoảng cách Manhattan giữa hai điểm
    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    # Khởi tạo hàng đợi chứa các ô cần kiểm tra
    queue = [(manhattan_distance(start, end), start)]

    # Khởi tạo bản đồ các ô đã được đi qua
    visited = set()
    visited.add(start)

    # Duyệt hàng đợi
    while queue:
        _, current = heapq.heappop(queue)
        if current == end:
            break

        # Duyệt các ô lân cận
        for dx, dy in directions:
            new_cell = (current[0] + dx, current[1] + dy)
            if 0 <= new_cell[0] < rows and 0 <= new_cell[1] < cols and table[new_cell[0]][new_cell[1]] not in (1, 4):
                if new_cell not in visited:
                    visited.add(new_cell)
                    heapq.heappush(
                        queue, (manhattan_distance(new_cell, end), new_cell))
    if end not in visited:
        return None  # Không tìm được đường đi
    # Tạo đường đi từ end đến start
    path = []
    current = end
    while current != start:
        path.append(current)
        min_dist = float('inf')
        min_cell = None
        for dx, dy in directions:
            new_cell = (current[0] + dx, current[1] + dy)
            if 0 <= new_cell[0] < rows and 0 <= new_cell[1] < cols and new_cell in visited and new_cell not in path:
                dist = manhattan_distance(new_cell, start)
                if dist < min_dist:
                    min_dist = dist
                    min_cell = new_cell
        current = min_cell
    path.append(start)
    path.reverse()

    return path


def find_path_A_Star(rows, cols, start, end, table):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1),
                  (1, -1), (1, 1)]  # Hướng di chuyển: phải, trái, xuống, lên

    # Khởi tạo hàng đợi chứa các ô cần kiểm tra
    queue = [(0, start)]

    # Khởi tạo bản đồ các ô đã được đi qua
    visited = set()
    visited.add(start)

    # Khởi tạo bản đồ đường đi từ start đến mỗi ô và giá trị f
    path_map = {start: (0, None)}

    # Duyệt hàng đợi
    while queue:
        _, current = heapq.heappop(queue)
        if current == end:
            break

        # Duyệt các ô lân cận
        for dx, dy in directions:
            new_cell = (current[0] + dx, current[1] + dy)
            if 0 <= new_cell[0] < rows and 0 <= new_cell[1] < cols and table[new_cell[0]][new_cell[1]] not in (1, 4):
                new_cost = path_map[current][0] + 1
                if new_cell not in visited or new_cost < path_map[new_cell][0]:
                    visited.add(new_cell)
                    heapq.heappush(
                        queue, (new_cost + manhattan_distance(new_cell, end), new_cell))
                    path_map[new_cell] = (new_cost, current)

    if end not in path_map:
        return None  # Không tìm được đường đi

    # Tạo đường đi từ end đến start
    path = []
    current = end
    while current != start:
        path.append(current)
        current = path_map[current][1]
    path.append(start)
    path.reverse()

    return path


def readFile(Map, robot, filename):
    global row, column

    with open(filename, "r") as file:
        line = file.readline().split(',')
        column = int(line[0]) + 1
        row = int(line[1]) + 1

        for i in range(row):
            r = []
            for j in range(column):
                if j == 0 or i == 0 or j == column - 1 or i == row - 1:
                    r.append(1)
                else:
                    r.append(0)

            Map.table.append(r)

        line = file.readline().split(',')
        robot.posi = row - 1 - int(line[1])
        robot.posj = int(line[0])

        Map.goal = (row - 1 - int(line[3]), int(line[2]))
        # set vị trí cho robot và đích

        line = file.readline().split(',')
        Map.num_polygon = int(line[0])

        for _ in range(Map.num_polygon):
            polygon = []

            line = file.readline().split(',')
            for i in range(0, len(line), 2):
                polygon.append((row - 1 - int(line[i + 1]), int(line[i])))

            Map.polygons.append(polygon)

        Map.table[robot.posi][robot.posj] = 2
        Map.table[Map.goal[0]][Map.goal[1]] = 3

        Map.checkpoint.append((robot.posi, robot.posj))
        line = file.readline().split(',')
        for i in range(0, len(line), 2):
            Map.checkpoint.append((row - 1 - int(line[i + 1]), int(line[i])))
        Map.checkpoint.append(Map.goal)


class TableGame:
    def __init__(self):
        self.table = []
        self.path = []
        self.length = 0
        self.width = 0
        self.num_polygon = 0
        self.polygons = []
        self.goal = (0, 0)
        self.checkpoint = []

    def checkWin(self):
        for i in range(0, row):
            for j in range(0, column):
                if (self.table[i][j] == 2):
                    return False
        return True

    def eucliean_distance(self, x1, y1, x2, y2):
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

    def match_two_point(self, point_1, point_2):
        polygon_path = []

        # vẽ đường thẳng nếu chung tung độ
        if point_1[0] == point_2[0]:
            for match in range(0, abs(point_1[1] - point_2[1]) + 1):
                if point_2[1] > point_1[1]:
                    self.table[point_1[0]][point_1[1] + match] = 1
                    polygon_path.append((point_1[0], point_1[1] + match))
                else:
                    self.table[point_1[0]][point_2[1] + match] = 1
                    polygon_path.append((point_1[0], point_2[1] + match))

        # vẽ đường thẳng nếu chung hoành độ
        elif point_1[1] == point_2[1]:
            for match in range(0, abs(point_1[0] - point_2[0]) + 1):
                if point_2[0] > point_1[0]:
                    self.table[point_1[0] + match][point_1[1]] = 1
                    polygon_path.append((point_1[0] + match, point_1[1]))

                else:
                    self.table[point_2[0] + match][point_1[1]] = 1
                    polygon_path.append((point_2[0] + match, point_1[1]))

        # breadth-first search
        else:
            positions = [
                (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
            x_next = point_1[0]
            y_next = point_1[1]
            while not (x_next == point_2[0] and y_next == point_2[1]):
                minimum = column * row
                x_tmp = x_next
                y_tmp = y_next
                for position in positions:
                    if 0 < x_next + position[0] < row and 0 < y_next + position[1] < column:
                        if x_next + position[0] == point_2[0] and y_next + position[1] == point_2[1]:
                            x_tmp = point_2[0]
                            y_tmp = point_2[1]
                            break

                        if self.table[x_next + position[0]][y_next + position[1]] == 0:
                            path_weight = round(self.eucliean_distance(
                                x_next + position[0], y_next + position[1], point_2[0], point_2[1]), 2)
                            if position[0] == 0 or position[1] == 0:
                                path_weight += 1

                            else:
                                path_weight += 1.50

                            if path_weight < minimum:
                                minimum = path_weight
                                x_tmp = x_next + position[0]
                                y_tmp = y_next + position[1]

                x_next = x_tmp
                y_next = y_tmp
                self.table[x_next][y_next] = 1
                polygon_path.append((x_next, y_next))

        return polygon_path

    def plotting_polygon(self, polygon):

        # tô điểm đầu tiên
        self.table[polygon[0][0]][polygon[0][1]] = 1
        # bỏ điểm đầu tiên vô path
        polygon_path = [(polygon[0][0], polygon[0][1])]

        # điền đường đi vào path
        for index in range(1, len(polygon)):
            curr = polygon[index]
            prev = polygon[index - 1]
            polygon_path.extend(self.match_two_point(prev, curr))

        # điền điểm cuối và điểm đầu
        polygon_path.extend(self.match_two_point(
            polygon[0], polygon[len(polygon) - 1]))
        return polygon_path

    def drawing_dynamic_polygon(self, polygon):

        self.table[polygon[0][0]][polygon[0][1]] = 1
        polygon_path = [(polygon[0][0], polygon[0][1])]
        save_side = []
        for index in range(1, len(polygon)):
            curr = polygon[index]
            prev = polygon[index - 1]
            side = self.match_two_point(prev, curr)
            if prev[1] < curr[1]:
                save_side.extend(side)

            polygon_path.extend(side)

        side = self.match_two_point(polygon[0], polygon[len(polygon) - 1])
        polygon_path.extend(side)
        table_polygon = []
        for up_side in save_side:
            for point in polygon_path:
                if up_side[1] == point[1]:
                    for k in range(point[0] + 1, up_side[0]):
                        table_polygon.append((k, up_side[1]))
        polygon_path.extend(table_polygon)
        return polygon_path

    def paint_inside_polygon(self, path):
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                if (i, j) not in path and any(point[0] > i for point in path) and any(point[0] < i for point in path) and any(point[1] > j for point in path) and any(point[1] < j for point in path):
                    self.table[i][j] = 4

    def moving_polygon(self, polygon, step):
        polygon_path = polygon[:]
        point_amount = len(polygon_path)
        for i in range(point_amount):
            if 0 < polygon_path[i][0] + step[0] < row and 0 < polygon_path[i][1] + step[1] < column:
                if self.table[polygon_path[i][0] + step[0]][polygon_path[i][1] + step[1]] == 1 \
                    or self.table[polygon_path[i][0] + step[0]][polygon_path[i][1] + step[1]] == 2 \
                        or self.table[polygon_path[i][0] + step[0]][polygon_path[i][1] + step[1]] == 3:
                    return False, []

                polygon_path[i] = (polygon_path[i][0] + step[0],
                                   polygon_path[i][1] + step[1])

            else:
                return False, []

        return True, polygon_path


class LevelChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')

        self.robot = pygame.transform.scale(
            pygame.image.load('./image/robot.png'), (50, 60))
        self.robot_x = 0
        self.robot_y = 0
        self.robot_dir = (1, 0)

        self.choice = 0
        self.isChoosing = True

    def drawChoose(self):
        global width, height
        x, y = pygame.mouse.get_pos()
        width, height = screen.get_size()
        self.bg = pygame.transform.scale(self.bg, (width, height))
        screen.blit(self.bg, (0, 0))

        robot_rect = self.robot.get_rect()
        # generate a robot which run on screen
        if random.randint(1, 50) == 25:
            self.robot_dir = random.choice(directions)
        self.robot_x += self.robot_dir[0] * 4
        self.robot_y += self.robot_dir[1] * 4
        # limit the running of robot on the screen
        if self.robot_x < 0:
            self.robot_x = width
        elif self.robot_x > width:
            self.robot_x = 0
        if self.robot_y < 0:
            self.robot_y = height
        elif self.robot_y > height:
            self.robot_y = 0

        screen.blit(self.robot, (self.robot_x, self.robot_y))

        font = pygame.font.SysFont('DroidSans', 50)
        color = (int(0), int(0), int(0))
        screen.blit(font.render("Welcome to Find Road Game.",
                    True, (color)), (width/2 - 235, 50))
        screen.blit(font.render("Let choose your level!",
                    True, (color)), (width/2 - 235, 98))

        if x > width/2-220 and x < width/2-20 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = 1
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-75, 200, 80), 8)
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-75, 200, 80), 8)
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = 3
            pygame.draw.rect(
                screen, color, (width/2-150, height/2 + 15, 250, 80), 8)
        else:
            self.select = 0

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Tìm đường", True, color), (width/2-180, height/2 - 40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Điểm đón", True, color), (width/2 + 70, height/2-40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Đa giác di chuyển", True, color), (width/2-120, height/2 + 48))
        pygame.display.flip()

    def choose(self):
        while self.isChoosing:
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.choice != 0:
                            self.isChoosing = False

                clock.tick(60)


class MapChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.robot = pygame.transform.scale(
            pygame.image.load('./image/robot.png'), (50, 60))
        self.robot_x = 0
        self.robot_y = 0
        self.robot_dir = (1, 0)

        self.choice = 0
        self.isChoosing = True

    def drawChoose(self):
        global width, height
        x, y = pygame.mouse.get_pos()
        width, height = screen.get_size()
        self.bg = pygame.transform.scale(self.bg, (width, height))
        screen.blit(self.bg, (0, 0))

        robot_rect = self.robot.get_rect()
        # generate a robot which run on screen
        if random.randint(1, 50) == 25:
            self.robot_dir = random.choice(directions)
        self.robot_x += self.robot_dir[0] * 4
        self.robot_y += self.robot_dir[1] * 4
        # limit the running of robot on the screen
        if self.robot_x < 0:
            self.robot_x = width
        elif self.robot_x > width:
            self.robot_x = 0
        if self.robot_y < 0:
            self.robot_y = height
        elif self.robot_y > height:
            self.robot_y = 0

        screen.blit(self.robot, (self.robot_x, self.robot_y))

        font = pygame.font.SysFont('DroidSans', 50)
        color = (int(0), int(0), int(0))
        screen.blit(font.render("Next Step: Choose a map!",
                    True, (color)), (width/2 - 200, 46))

        if x > width/2-220 and x < width/2-20 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = 1
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-75, 200, 80), 8)
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-75, 200, 80), 8)
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = 3
            pygame.draw.rect(
                screen, color, (width/2-150, height/2 + 15, 250, 80), 8)
        else:
            self.select = 0

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 1", True, color), (width/2-180, height/2 - 40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 2", True, color), (width/2 + 70, height/2-40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 3 (No path)", True, color), (width/2-120, height/2 + 48))
        pygame.display.flip()

    def choose(self):
        while self.isChoosing:
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.choice != 0:
                            self.isChoosing = False

                clock.tick(60)


class AlgorithmChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.robot = pygame.transform.scale(
            pygame.image.load('./image/robot.png'), (50, 60))
        self.robot_x = 0
        self.robot_y = 0
        self.robot_dir = (1, 0)

        self.choice = 0
        self.isChoosing = True

    def drawChoose(self):
        global width, height
        x, y = pygame.mouse.get_pos()
        width, height = screen.get_size()
        self.bg = pygame.transform.scale(self.bg, (width, height))
        screen.blit(self.bg, (0, 0))

        robot_rect = self.robot.get_rect()
        # generate a robot which run on screen
        if random.randint(1, 50) == 25:
            self.robot_dir = random.choice(directions)
        self.robot_x += self.robot_dir[0] * 4
        self.robot_y += self.robot_dir[1] * 4
        # limit the running of robot on the screen
        if self.robot_x < 0:
            self.robot_x = width
        elif self.robot_x > width:
            self.robot_x = 0
        if self.robot_y < 0:
            self.robot_y = height
        elif self.robot_y > height:
            self.robot_y = 0

        screen.blit(self.robot, (self.robot_x, self.robot_y))

        font = pygame.font.SysFont('DroidSans', 50)
        color = (int(0), int(0), int(0))
        screen.blit(font.render("Final: Choose an algorithm!",
                    True, (color)), (width/2 - 235, 50))

        if x > width/2-220 and x < width/2-20 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = find_path_A_Star
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-75, 200, 80), 8)
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = find_path_greedy
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-75, 200, 80), 8)
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = find_path_bfs
            pygame.draw.rect(
                screen, color, (width/2-120, height/2 + 15, 200, 80), 8)
        else:
            self.select = 0

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "A Star", True, color), (width/2-160, height/2 - 40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Greedy Search", True, color), (width/2 + 48, height/2-40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "BFS", True, color), (width/2-40, height/2 + 48))
        pygame.display.flip()

    def choose(self):
        while self.isChoosing:
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.choice != 0:
                            self.isChoosing = False

                clock.tick(60)


class PlayGame:
    def __init__(self):
        self.isplay = False
        self.bg = pygame.image.load("./image/bg.jpg")

    def handle_game(self, level, map, algo):
        def drawCheckPoint():
            for point in Map.checkpoint[1:]:
                pygame.draw.rect(screen, (255, 0, 0), (point[1] * width_rec +
                                                       x_root + 1, point[0] * width_rec + y_root + 1, width_rec - 2, width_rec - 2))

        def drawGoal():
            pygame.draw.rect(screen, (255, 0, 0), (Map.goal[1] * width_rec +
                                                   x_root + 1, Map.goal[0] * width_rec + y_root + 1, width_rec - 2, width_rec - 2))

        def drawPath(path):
            for cell in path:
                pygame.draw.rect(screen, (255, 182, 193), (cell[1] * width_rec +
                                                           x_root + 1, cell[0] * width_rec + y_root + 1, width_rec - 2, width_rec - 2))

        def draw(robot):
            randomcolor = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            # screen.blit(self.bg, (0, 0))
            drawWall()
            drawPath(robot.direction_queue)
            drawCheckPoint()
            drawGoal()
            drawRobot(robot)
            if Map.table[robot.posi][robot.posj] == 3:
                self.isplay = False

            pygame.draw.rect(screen, (0, 38, 230), (50, 50, 150, 70), 5)

        def drawlv3(robot, amount):
            polygon_steps = [(-1, 0), (1, 0), (0, 1), (0, -1)]

            # screen.blit(self.bg, (0, 0))
            drawWall()
            drawPath(robot.direction_queue)
            drawGoal()
            if drawRobot(robot):
                if Map.table[robot.posi][robot.posj] == 3:
                    self.isplay = False
                Map.table[robot.posi][robot.posj] = 2

                index_border = 0
                tmp_step = polygon_steps[:]
                while index_border < amount:
                    if tmp_step:
                        step = random.choice(tmp_step)
                        tmp_step.remove(step)
                        for point in polygon_borders[index_border]:
                            Map.table[point[0]][point[1]] = 0
                        ok_step, tmp_border = Map.moving_polygon(
                            polygon_borders[index_border], step)
                        if ok_step:
                            polygon_borders[index_border] = tmp_border
                            for point in polygon_borders[index_border]:
                                Map.table[point[0]][point[1]] = 1
                            Map.paint_inside_polygon(
                                polygon_borders[index_border])
                            index_border += 1
                        else:
                            for point in polygon_borders[index_border]:
                                Map.table[point[0]][point[1]] = 1
                    else:
                        index_border += 1

                    robot.direction_queue = algo(
                        row, column, (robot.posi, robot.posj), (Map.goal), Map.table)[1:]

            if Map.table[robot.posi][robot.posj] == 3:
                self.isplay = False
            Map.table[robot.posi][robot.posj] = 2

            pygame.draw.rect(screen, (0, 38, 230), (50, 50, 150, 70), 5)

        def drawRobot(robot):
            screen.blit(robot.robot_image, (robot.posj * width_rec +
                                            x_root + robot.posx + width_rec/4 + 1, robot.posi * width_rec + y_root + robot.posy + width_rec/4 + 1, width_rec - 2, width_rec - 2))
            if self.isplay:
                return robot.move()

        def drawWall():
            wall_color = (0, 38, 230)  # Color for the walls
            for i in range(row):
                for j in range(column):
                    pygame.draw.rect(screen, (0, 0, 0), (j * width_rec +
                                                         x_root, i * width_rec + y_root, width_rec, width_rec))

                    if Map.table[i][j] == 1:  # Check if the cell contains a wall
                        # Draw a rectangle for the wall
                        # screen.blit(pygame.transform.scale(pygame.image.load(
                        #     "./image/pacman.png"), (width_rec/2, width_rec/2)), (j * width_rec +
                        #                                                          x_root, i * width_rec + y_root, width_rec, width_rec))

                        pygame.draw.rect(screen, wall_color, (j * width_rec +
                                                              x_root + 1, i * width_rec + y_root + 1, width_rec - 2, width_rec - 2))
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), (j * width_rec +
                                                                   x_root + 1, i * width_rec + y_root + 1, width_rec - 2, width_rec - 2))  # Assuming (0, 0, 0) is the color for removal

        Map = TableGame()
        robot = Robot()
        self.isplay = True

        if level == 1:
            try:
                readFile(Map, robot, "./map/" + str(map) + ".txt")
                Map.checkpoint = []
                for polygon in Map.polygons:
                    path = Map.plotting_polygon(polygon)
                    Map.paint_inside_polygon(path)

                robot.direction_queue = algo(
                    row, column, (robot.posi, robot.posj), (Map.goal), Map.table)[1:]

                while self.isplay:
                    width, height = screen.get_size()
                    x_root = width/2 - column * width_rec/2
                    y_root = height/2 - row*width_rec/2
                    draw(robot)

                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    clock.tick(FPS)
                    pygame.display.update()
            except:
                width, height = screen.get_size()
                x_root = width/2 - column * width_rec/2
                y_root = height/2 - row*width_rec/2
                self.isplay = False
                drawWall()
                drawRobot(robot)
                font = pygame.font.SysFont('DroidSans', 50)
                color = (int(255), int(0), int(0))
                screen.blit(font.render("No Path FOUND!!!",
                            True, (color)), (width/2 - 200, 98))
                pygame.draw.rect(screen, (0, 38, 230), (50, 50, 150, 70), 5)
                pygame.display.flip()
                time.sleep(5)

        elif level == 2:
            try:
                readFile(Map, robot, "./map/" + str(map) + ".txt")
                for point in Map.checkpoint[1:]:
                    Map.table[point[0]][point[1]] = 3

                for polygon in Map.polygons:
                    path = Map.plotting_polygon(polygon)
                    Map.paint_inside_polygon(path)

                paths = []

                for i in range(len(Map.checkpoint)-1):
                    paths.append(algo(
                        row, column, Map.checkpoint[i], Map.checkpoint[i+1], Map.table)[1:])

                while self.isplay:
                    for p in paths:
                        self.isplay = True
                        robot.direction_queue = p
                        Map.table[robot.posi][robot.posj] = 2
                        while self.isplay:
                            width, height = screen.get_size()
                            x_root = width/2 - column * width_rec/2
                            y_root = height/2 - row*width_rec/2
                            draw(robot)

                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            clock.tick(FPS)
                            pygame.display.update()

            except:
                width, height = screen.get_size()
                x_root = width/2 - column * width_rec/2
                y_root = height/2 - row*width_rec/2
                self.isplay = False
                drawWall()
                drawRobot(robot)
                font = pygame.font.SysFont('DroidSans', 50)
                color = (int(255), int(0), int(0))
                screen.blit(font.render("No Path FOUND!!!",
                            True, (color)), (width/2 - 200, 98))
                pygame.draw.rect(screen, (0, 38, 230), (50, 50, 150, 70), 5)
                pygame.display.flip()
                time.sleep(5)

        elif level == 3:
            try:
                Map.checkpoint = []

                readFile(Map, robot, "./map/" + str(map) + ".txt")

                polygon_borders = []
                for polygon in Map.polygons:
                    border = Map.drawing_dynamic_polygon(polygon)
                    polygon_borders.append(border)
                    Map.paint_inside_polygon(border)

                robot.direction_queue = algo(
                    row, column, (robot.posi, robot.posj), (Map.goal), Map.table)[1:]
                while self.isplay:

                    width, height = screen.get_size()
                    x_root = width/2 - column * width_rec/2
                    y_root = height/2 - row*width_rec/2
                    drawlv3(robot, len(polygon_borders))

                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    clock.tick(FPS)
                    pygame.display.update()
            except:
                width, height = screen.get_size()
                x_root = width/2 - column * width_rec/2
                y_root = height/2 - row*width_rec/2
                self.isplay = False
                drawWall()
                drawRobot(robot)
                font = pygame.font.SysFont('DroidSans', 50)
                color = (int(255), int(0), int(0))
                screen.blit(font.render("No Path FOUND!!!",
                            True, (color)), (width/2 - 200, 98))
                pygame.draw.rect(screen, (0, 38, 230), (50, 50, 150, 70), 5)
                pygame.display.flip()
                time.sleep(5)


while True:
    levelChooser = LevelChooser()
    levelChooser.choose()
    mapChooser = MapChooser()
    mapChooser.choose()

    algorithmChooser = AlgorithmChooser()
    algorithmChooser.choose()

    game = PlayGame()
    game.handle_game(levelChooser.choice, mapChooser.choice,
                     algorithmChooser.choice)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(60)
    pygame.display.update()
