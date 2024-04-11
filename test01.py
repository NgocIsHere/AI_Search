import pygame
import sys
import heapq
from collections import deque
from itertools import permutations

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

# Hàm tìm đường đi từ start đến end không đi vào các ô đã tô màu và không đi lên cạnh, sử dụng thuật toán A*
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

################################################
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
    return (row >= 0) and (row < len(map)) and \
    (col >= 0) and (col < len(map[0])) and \
    (map[row][col] == 0)

def bfs_level1(rows, cols, start_point, end_point, colored_cells):
    map = [[0 for _ in range(cols)] for _ in range(rows)]
    for cell in colored_cells:
        col, row = cell
        if 0 <= row < rows and 0 <= col < cols:
            map[row][col] = '#'

    print(map)

    visited = [[False] * len(map[0]) for i in range(len(map))]

    steps = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # up, down, left, right, north-west, north-east, south-west, south-east

    queue = deque([(start_point[0], start_point[1], 0, [])]) #(row, col, cost, path)
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
                        return (cost, newPath)
                    else:
                        queue.append((next_row, next_col, cost, newPath))
                        visited[next_row][next_col] = True

    return None



def main():
    # Đọc dữ liệu từ file
    filename = 'map/input.txt'  # Thay 'input.txt' bằng tên file cụ thể
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
        
        # A*:
        # path = find_path(rows, cols, start_point, end_point, colored_cells)
        
        # Greedy:
        path = find_path_greedy(rows, cols, start_point, end_point, colored_cells)
        
        # DFS:
        # path = find_path_dfs(rows, cols, start_point, end_point, colored_cells)
        
        # BFS:
        path = bfs_level1(rows, cols, start_point, end_point, colored_cells)
        # print(path)
        if  path == None:
            running = False
        else:
            draw_path(screen, path[1], cell_width, cell_height)
            
        pygame.display.flip()  
        pygame.time.delay(10000)
        running = False
    pygame.quit() 


if __name__ == "__main__":
    main()
