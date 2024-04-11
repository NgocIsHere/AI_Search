import pygame
import random
import pygame
import sys
import heapq
from collections import deque
from itertools import permutations

pygame.init()
clock = pygame.time.Clock()
width = 1280
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
              (1, 1), (-1, -1), (1, -1), (-1, 1)]


class LevelChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.maplv1 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv2 = pygame.transform.scale(
            pygame.image.load('./image/maplv2.png'), (200, 150))
        self.maplv3 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv4 = pygame.transform.scale(
            pygame.image.load('./image/maplv4.png'), (200, 150))
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
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-175, 210, 160))
            self.choice = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-175, 210, 160))
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = 3
            pygame.draw.rect(
                screen, color, (width/2-225, height/2 + 15, 210, 160))
        elif x > width/2+20 and x < width/2+220 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = 4
            pygame.draw.rect(
                screen, color, (width/2+15, height/2+15, 210, 160))
        else:
            self.choice = 0

        screen.blit(self.maplv1, (width/2-220, height/2-170))
        screen.blit(self.maplv2, (width/2+20, height/2-170))
        screen.blit(self.maplv3, (width/2-220, height/2+20))
        screen.blit(self.maplv4, (width/2+20, height/2+20))

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 1", True, color), (width/2-160, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 2", True, color), (width/2 + 80, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 3", True, color), (width/2-160, height/2 + 175))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 4", True, color), (width/2 + 80, height/2 + 175))
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
        self.maplv1 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv2 = pygame.transform.scale(
            pygame.image.load('./image/maplv2.png'), (200, 150))
        self.maplv3 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
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
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-175, 210, 160))
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.select = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-175, 210, 160))
        elif x > width/2-110 and x < width/2+100 and y > height/2 + 20 and y < height/2 + 170:
            self.select = 3
            pygame.draw.rect(
                screen, color, (width/2-115, height/2 + 15, 210, 160))
        else:
            self.select = 0

        screen.blit(self.maplv1, (width/2-220, height/2-170))
        screen.blit(self.maplv2, (width/2+20, height/2-170))
        screen.blit(self.maplv3, (width/2-110, height/2+20))

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 1", True, color), (width/2-160, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 2", True, color), (width/2 + 80, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 3 (No path)", True, color), (width/2-80, height/2 + 175))
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
                        if self.select != 0:
                            self.isChoosing = False

                clock.tick(60)


class AlgorithmChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.maplv1 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv2 = pygame.transform.scale(
            pygame.image.load('./image/maplv2.png'), (200, 150))
        self.maplv3 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv4 = pygame.transform.scale(
            pygame.image.load('./image/maplv4.png'), (200, 150))
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
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-75, 200, 80), 8)
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.select = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-75, 200, 80), 8)
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.select = 3
            pygame.draw.rect(
                screen, color, (width/2-120, height/2 + 15, 200, 80), 8)
        else:
            self.select = 0

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "A Star", True, color), (width/2-160, height/2 - 40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Greedy", True, color), (width/2 + 48, height/2-40))
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
                        if self.select != 0:
                            self.isChoosing = False

                clock.tick(60)

# Hàm đọc dữ liệu từ file
def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Đọc số hàng và số cột
        rows, cols = map(int, lines[0].split())
        
        # Đọc điểm bắt đầu và kết thúc
        start_point = tuple(map(int, lines[1].split()))
        end_point = tuple(map(int, lines[2].split()))
        
        # Đọc số đa giác
        num_polygons = int(lines[3])
        
        # Đọc tọa độ các điểm trên các đa giác
        polygons = []
        for line in lines[4:]:
            points = list(map(int, line.split()))
            polygons.append([(points[i], points[i+1]) for i in range(0, len(points), 2)])
        
    return rows, cols, start_point, end_point, num_polygons, polygons

# Hàm vẽ các đa giác và các điểm bắt đầu/kết thúc
def draw_objects(screen, rows, cols, start_point, end_point, polygons):
    # Tính kích thước của ô
    cell_width = screen.get_width() // cols
    cell_height = screen.get_height() // rows
    
    # Danh sách các ô đã được tô màu
    colored_cells = set()
    
    # Vẽ lưới caro và tô màu các ô
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * cell_width, i * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            if i==0 or j ==0 or i== rows-1 or j == cols-1:
                pygame.draw.rect(screen, (200, 200, 200), rect)
    # Tô màu các ô mà chứa các điểm của các đa giác và vẽ cạnh của đa giác
    for polygon in polygons:
        # Vẽ các cạnh của đa giác
        for i in range(len(polygon)):
            start = polygon[i]
            end = polygon[(i + 1) % len(polygon)]
            draw_line(screen, start, end)
            # Thêm các ô đã được tô màu vào danh sách
            colored_cells.update(get_cells_between(start, end))
        
        # Tô màu các ô chứa các điểm của đa giác
        for point in polygon:
            x, y = point
            rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, (255, 0, 0), rect)
    
    # Vẽ điểm bắt đầu và điểm kết thúc
    start_x, start_y = start_point
    end_x, end_y = end_point
    start_x = start_x * cell_width + cell_width // 2
    start_y = start_y * cell_height + cell_height // 2
    end_x = end_x * cell_width + cell_width // 2
    end_y = end_y * cell_height + cell_height // 2
    pygame.draw.circle(screen, (0, 255, 0), (start_x, start_y), 5)
    pygame.draw.circle(screen, (0, 0, 255), (end_x, end_y), 5)
    
    # Tô màu các ô đã được tô màu
    for cell in colored_cells:
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(cell[0] * cell_width, cell[1] * cell_height, cell_width, cell_height))
    return colored_cells
# Hàm vẽ đường thẳng giữa hai điểm
def draw_line(screen, start, end):
    # Lấy tọa độ của điểm bắt đầu và kết thúc
    x1, y1 = start
    x2, y2 = end
    
    # Tính độ lệch theo x và y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Xác định hướng di chuyển của đường thẳng
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    # Tính sai số
    err = dx - dy
    
    # Vẽ các điểm trên đường thẳng
    while True:
        pygame.draw.rect(screen, (0, 0, 0), (x1 * screen.get_width(), y1 * screen.get_width(), screen.get_width(), screen.get_width()))
        
        # Điểm cuối đã đạt được
        if x1 == x2 and y1 == y2:
            break
        
        # Tính sai số tiếp theo
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Hàm tính các ô nằm giữa hai điểm
def get_cells_between(start, end):
    cells = set()
    x1, y1 = start
    x2, y2 = end
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    err = dx - dy
    
    while True:
        cells.add((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    
    return cells
# Hàm vẽ đường đi trên map
def draw_path(screen, path, cell_width, cell_height):
    for cell in path:
        x, y = cell
        rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
        font = pygame.font.Font(None, 25)
        text = font.render('X', True, (0, 0, 0))
        screen.blit(text, (x * cell_width + cell_width // 3, y * cell_height + cell_height // 3))

def Start():
    levelChooser = LevelChooser()
    levelChooser.choose()
    mapChooser = MapChooser()
    mapChooser.choose()

    algorithmChooser = AlgorithmChooser()
    if levelChooser.choice != 1:
        algorithmChooser.choose()
    else:
        algorithmChooser.choice = 1
    return (levelChooser.choice, algorithmChooser.choice,mapChooser.choice)

# Hàm tìm đường đi từ start đến end sử dụng thuật toán A*
def find_path(rows, cols, start, end, colored_cells):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Hướng di chuyển: phải, trái, xuống, lên
    
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
            if 0 <= new_cell[0] < cols and 0 <= new_cell[1] < rows and new_cell not in colored_cells:
                new_cost = path_map[current][0] + 1
                if new_cell not in visited or new_cost < path_map[new_cell][0]:
                    visited.add(new_cell)
                    heapq.heappush(queue, (new_cost + manhattan_distance(new_cell, end), new_cell))
                    path_map[new_cell] = (new_cost, current)
    
    # Kiểm tra xem có tìm được đường đi từ start đến end không
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

# Hàm tính khoảng cách Manhattan giữa hai điểm
def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Hàm tìm đường đi từ start đến end không đi vào các ô đã tô màu và không đi lên cạnh, sử dụng thuật toán Greedy:
def find_path_greedy(rows, cols, start, end, colored_cells):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Hướng di chuyển: phải, trái, xuống, lên
    
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
            if 0 <= new_cell[0] < cols and 0 <= new_cell[1] < rows and new_cell not in colored_cells:
                if new_cell not in visited:
                    visited.add(new_cell)
                    heapq.heappush(queue, (manhattan_distance(new_cell, end), new_cell))
    
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
            if 0 <= new_cell[0] < cols and 0 <= new_cell[1] < rows and new_cell in visited:
                dist = manhattan_distance(new_cell, start)
                if dist < min_dist:
                    min_dist = dist
                    min_cell = new_cell
        current = min_cell
    path.append(start)
    path.reverse()
    
    return path
# Hàm tìm đường đi từ start đến end không đi vào các ô đã tô màu và không đi lên cạnh, sử dụng thuật toán DFS
def find_path_dfs(rows, cols, start, end, colored_cells):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Hướng di chuyển: phải, trái, xuống, lên
    
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
            if 0 <= new_cell[0] < cols and 0 <= new_cell[1] < rows and new_cell not in colored_cells and new_cell not in visited:
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
# BFS:
def can_move(map, row, col):
    # Kiểm tra xem ô có nằm ngoài biên không và không phải là ô tô màu
    return 0 <= row < len(map) and 0 <= col < len(map[0]) and map[row][col] != 'X'

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

    if len(must_passes) == 0:
        return bfs_level1(map, start, goal)

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
        if not res:
            continue
        gap += res[0] #khoảng cách giữa start và điểm đón đầu tiên
        new_path += res[1]
        for i in range(len(must_passes) - 1):
            distance = d[permutation[i]][permutation[i + 1]] #khoảng cách giữa các điểm đón
            if not distance: # nếu mà không tồn tài đường đi giữa hai điểm đón thì bỏ path này
                continue
            gap += distance[0]
            new_path += d[permutation[i]][permutation[i + 1]][1][1:]
        res = bfs_level1(map.copy(), must_passes[permutation[sz - 1]], goal)
        if not res:
            continue
        gap += res[0] # khoảng cách giữa điểm đón cuối cùng và goal
        new_path += res[1][1:]

        if(gap < shortest):
            shortest = gap
            shortest_path = new_path

    if len(shortest_path) == 0:
        return None
    return (shortest, shortest_path)
def main():
    # Đọc dữ liệu từ file
    level,alg,map = Start()
    # filename = "map/input"+ str(map) +".txt"
    

    filename = 'map/input.txt' 
    filename2 = 'map/input.txt'
    filename3 = 'map/input.txt'
    rows, cols, start_point, end_point, num_polygons, polygons = read_input(filename)
    
    # Khởi tạo Pygame
    pygame.init()
    

    # Kích thước cửa sổ
    window_size = (400, 400)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Vẽ đối tượng từ file')

    # Tính kích thước của ô
    cell_width = screen.get_width() // cols
    cell_height = screen.get_height() // rows

    # Danh sách các ô đã được tô màu
    colored_cells = set()

    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * cell_width, i * cell_height, cell_width, cell_height)
            if i==0 or j ==0 or i== rows-1 or j == cols-1:
                pygame.draw.rect(screen, (200, 200, 200), rect)
                colored_cells.add((j,i))

    for polygon in polygons:
        for point in polygon:
            colored_cells.add(point)

    # Vòng lặp chính
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill((255, 255, 255))  # Xóa màn hình
            
        # Vẽ các đối tượng
        colored_cells.update(draw_objects(screen, rows, cols, start_point, end_point, polygons))
        if level == 1 :
            print("level 1")
            ###############################################################
            # path = find_path(rows, cols, start_point, end_point, colored_cells)
            path = find_path_greedy(rows, cols, start_point, end_point, colored_cells)
            
            # path = find_path_dfs(rows, cols, start_point, end_point, colored_cells) 
            map = [[0 for _ in range(cols)] for _ in range(rows)]
            for cell in colored_cells:
                col, row = cell
                if 0 <= row < rows and 0 <= col < cols:
                    map[row][col] = '#'

            print(map)
            must_passes = [(1, 1), (5, 5), (6, 6)]
            # cost, path = bfs_level3(map.copy(), start_point, end_point, must_passes)
            # print(cost, path)
        elif level == 2:
            print("level 2")
            if alg == 0:
                path = find_path(rows, cols, start_point, end_point, colored_cells)
            elif alg == 1:
                path = find_path_greedy(rows, cols, start_point, end_point, colored_cells)
            elif alg == 2:
                path = find_path_dfs(rows, cols, start_point, end_point, colored_cells)
        elif level == 3:
            print("level 3")
        else:
            print("level 4")
        
        if  path == None:
            running = False
        else:
            draw_path(screen, path, cell_width, cell_height)
            
        pygame.display.flip()  
        pygame.time.delay(10000)
        running = False
        # Start()
    pygame.quit() 


if __name__ == "__main__":
    main()
