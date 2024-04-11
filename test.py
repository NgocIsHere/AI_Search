import pygame
import sys

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
    
    # Danh sách các ô đã được đa giác đè lên
    covered_cells = set()
    
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
            
            # Thêm các ô đã được đa giác đè lên vào danh sách
            covered_cells.update(get_cells_between(start, end))
        
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
    # Tô màu các ô bị đa giác đè lên
    for cell in covered_cells:
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(cell[0] * cell_width, cell[1] * cell_height, cell_width, cell_height))
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
    
    # Vòng lặp chính
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Xóa màn hình
        
        # Vẽ các đối tượng
        draw_objects(screen, rows, cols, start_point, end_point, polygons)
        
        pygame.display.flip()  # Cập nhật màn hình
    
    pygame.quit()

if __name__ == "__main__":
    main()
