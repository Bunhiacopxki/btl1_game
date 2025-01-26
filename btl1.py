import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie")

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
WHITE_BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

# Level
LEVELS = {
    'easy': 7000,
    'medium': 5000,
    'difficult': 4000
}
font = pygame.font.SysFont("comicsansms", 50)

# font = pygame.font.Font("Chillerz.otf", 50)
selected_level = None

# In Level ra màn hình
def draw_menu():
    screen.fill(WHITE)
    title_text = font.render("Welcome to my game", True, BLACK)
    bar_text = font.render("Choose your level", True, BLACK)
    easy_text = font.render("Easy", True, BLACK)
    medium_text = font.render("Medium", True, BLACK)
    difficult_text = font.render("Difficult", True, BLACK)
    title_rect = title_text.get_rect(center = (WIDTH//2, HEIGHT//2 - 250))
    bar_rect = bar_text.get_rect(center = (WIDTH//2, HEIGHT//2 - 200))
    easy_rect = easy_text.get_rect(center = (WIDTH//2, HEIGHT//2 - 100))
    medium_rect = medium_text.get_rect(center = (WIDTH//2, HEIGHT//2))
    difficult_rect = difficult_text.get_rect(center = (WIDTH//2, HEIGHT//2 + 100))
    screen.blit(title_text, title_rect)  # blit: Vẽ text vào vị trí rect
    screen.blit(bar_text, bar_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(difficult_text, difficult_rect)
    pygame.display.flip()
    return easy_rect, medium_rect, difficult_rect

# Xử lý sự kiện chọn level
choosing_level = True
while choosing_level:
    easy_rect, medium_rect, difficult_rect = draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if easy_rect.collidepoint(x, y):
                selected_level = 'easy'
            elif medium_rect.collidepoint(x, y):
                selected_level = 'medium'
            elif difficult_rect.collidepoint(x, y):
                selected_level = 'difficult'
            if selected_level:
                choosing_level = False

disappear_time = LEVELS[selected_level]

# Định nghĩa lớp Zombie với từng bộ phận riêng biệt
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, delay):
        super().__init__()
        self.x = x
        self.y = y
        self.delay = delay
        self.start = pygame.time.get_ticks()  # Thời điểm bất đầu
        self.is_rising = False  # Trạng thái trồi lên
        self.dead = False
        self.visible_parts = 0
        self.grave_shown = False
        self.head_rect = pygame.Rect(self.x + 20, self.y, 60, 60)
        
    def draw(self, screen):
        self.parts = [] # Danh sách chứa các phần của zombie để kiểm tra va chạm
        
        if self.visible_parts >= 1:
            # Đầu
            self.parts.append(self.head_rect)
            pygame.draw.rect(screen, GREEN, self.head_rect)  # Đầu zombie
            left_eye = pygame.Rect(self.x + 30, self.y + 25, 15, 8)
            pygame.draw.rect(screen, BLACK, left_eye)  # Mắt trái
            right_eye = pygame.Rect(self.x + 55, self.y + 25, 15, 8)
            pygame.draw.rect(screen, BLACK, right_eye)  # Mắt phải
            pygame.draw.line(screen, BLACK, (self.x + 30, self.y + 45), (self.x + 70, self.y + 45), 8)  # Miệng
        
            # Tóc
            pygame.draw.rect(screen, (0, 50, 0), (self.x + 20, self.y, 60, 10))
            pygame.draw.rect(screen, (0, 50, 0), (self.x + 20, self.y + 10, 20, 10))
            pygame.draw.rect(screen, (0, 50, 0), (self.x + 70, self.y + 10, 10, 10))
        
        if self.visible_parts >= 2:  
            # Thân
            body = pygame.Rect(self.x + 25, self.y + 60, 50, 80)
            self.parts.append(body)
            pygame.draw.rect(screen, WHITE_BLUE, body)  # Thân

        if self.visible_parts >= 3:
            # Tay
            left_leg = pygame.Rect(self.x + 5, self.y + 60, 20, 60)
            self.parts.append(left_leg)
            pygame.draw.rect(screen, GREEN, left_leg)  # Tay trái
            pygame.draw.rect(screen, WHITE_BLUE, (self.x + 5, self.y + 60, 20, 15))  # Tay áo trái
            right_leg = pygame.Rect(self.x + 75, self.y + 60, 20, 60)
            self.parts.append(right_leg)
            pygame.draw.rect(screen, GREEN, right_leg)  # Tay phải
            pygame.draw.rect(screen, WHITE_BLUE, (self.x + 75, self.y + 60, 20, 15))  # Tay áo phải
        
        if self.visible_parts >= 4:
            # Chân
            left_leg = pygame.Rect(self.x + 25, self.y + 140, 20, 50)
            self.parts.append(left_leg)
            pygame.draw.rect(screen, BLUE, left_leg)  # Chân trái
            pygame.draw.rect(screen, GREEN, (self.x + 25, self.y + 190, 20, 15))  # Chân trái
            right_leg = pygame.Rect(self.x + 55, self.y + 140, 20, 50)
            self.parts.append(right_leg)
            pygame.draw.rect(screen, BLUE, right_leg)  # Chân phải
            pygame.draw.rect(screen, GREEN, (self.x + 55, self.y + 190, 20, 15))  # Chân phải

        return self.parts

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Hiển thị ngôi mộ trước zombie
        if not self.grave_shown and current_time - self.start > self.delay - 1000:
            self.grave_shown = True
        
        # Kích hoạt hiệu ứng trồi lên sau khi hết delay
        if not self.is_rising and current_time - self.start > self.delay:
            self.is_rising = True

        # Tăng dần khi trồi lên và hiện dần từng bộ phận
        if self.is_rising:
            if self.visible_parts < 4:
                self.visible_parts += 1
            elif current_time - self.start > disappear_time: #  Xuất hiện 5s rồi die
                self.dead = True

        return self.dead
       
# Định nghĩa và thiết kế lớp Grave    
class Grave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y + 69, 100, 136)

    def draw(self, screen):
        # Phần thân ngôi mộ
        pygame.draw.rect(screen, GRAY, self.rect)
        # Phần đầu ngôi mộ
        pygame.draw.circle(screen, GRAY, (self.x + 50, self.y + 69), 50)
        # Chữ trên mộ
        rip_text = font.render("RIP", True, BLACK)
        screen.blit(rip_text, (self.x + 21, self.y + 88))
        

class Hammer:
    def __init__(self):
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.rotated_image = self.image  # Ảnh mặc định
        self.angle = 0  # Góc quay mặc định
        self.mouse_pressed = False
        
        # Vẽ búa
        self.draw_hammer_shape()

    # Vẽ hình cái búa lên Surface
    def draw_hammer_shape(self):
        # Xóa nền
        self.image.fill((0, 0, 0, 0))
        # Đầu búa (màu xám)
        pygame.draw.rect(self.image, GRAY, (40, 10, 60, 20))
        # Cán búa (màu nâu)
        pygame.draw.rect(self.image, BROWN, (65, 30, 15, 80))

    def update_rotation(self, angle):
        # Cập nhật góc quay của búa
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    def draw_cursor(self, screen, pos):
        # Vẽ búa tại vị trí con trỏ chuột
        rotated_rect = self.rotated_image.get_rect(center = pos)
        screen.blit(self.rotated_image, rotated_rect.topleft)
        self.head_rect = rotated_rect
        
    def check_collision(self, obj):
        if isinstance(obj, Zombie) and obj.is_rising:
            return self.mouse_pressed and self.angle != 0 and self.head_rect.colliderect(obj.head_rect)
        else:
            return self.mouse_pressed and self.angle != 0 and self.head_rect.colliderect(obj.rect)
        return False
        

############### Lớp bomb ################
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.start = pygame.time.get_ticks()  # Thời điểm bất đầu
        image_path = ['bomb.png', 'bomb2.png', 'zombom.jpg', 'zombom2.jpg']
        img = random.randint(0, len(image_path) - 1)
        # Tải ảnh bomb và lưu trữ trong thuộc tính image
        self.image = pygame.image.load('./img/' + image_path[img]).convert_alpha()  # Hỗ trợ ảnh trong suốt

        
        original_width, original_height = self.image.get_size()
        # Chiều cao mới
        new_height = 100
        # Tính toán chiều rộng mới dựa trên tỉ lệ ban đầu
        new_width = int((new_height / original_height) * original_width)
        # Scale ảnh với chiều rộng và chiều cao mới
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Lấy rect từ hình ảnh để định vị
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        # Vẽ hình ảnh lên màn hình
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.start > disappear_time #  Xuất hiện 5s rồi die



############### Lớp tính điểm ###############
class Point:
    def __init__(self):
        self.hit = 0
        self.miss = 0
        self.life = 3
    
    def getPoint(self):
        return self.hit
    
    def getLife(self):
        return self.life

    def getHitRate(self):
        if (self.hit + self.miss == 0 or self.hit < 0): return 0
        return float(self.hit)/(self.hit + self.miss)

# Ẩn con trỏ chuột mặc định
pygame.mouse.set_visible(False)

# Khởi tạo đối tượng búa
hammer = Hammer()
                      
# Tạo nhiều zombie và bomb ngẫu nhiên
def create_object(objs):
    while True:
        # Tạo ngẫu nhiên vị trí cho đối tượng
        x = random.randint(0, WIDTH - 100)
        y = random.randint(0, HEIGHT - 205)

        # Tạo rect của đối tượng mới (giả sử kích thước tối đa là 100x200)
        new_rect = pygame.Rect(x, y, 200, 210)

        # Kiểm tra khoảng cách giữa rect mới và rect của các đối tượng hiện có
        if all(not new_rect.colliderect(obj.rect) for obj in objs):
            # Xác định loại đối tượng dựa trên tỉ lệ 3:7
            if random.random() < 0.7:  # 70% khả năng xuất hiện Zombie
                zombie = Zombie(x, y, 2900)
                zombie.rect = new_rect  # Gán rect để sử dụng sau
                return zombie
            else:  # 30% khả năng xuất hiện Bomb
                bomb = Bomb(x, y)
                bomb.rect = new_rect  # Gán rect để sử dụng sau
                return bomb



game_time = 30000
num_of_object = 5
objs = []
spawn_timer = pygame.time.get_ticks()
# Thời gian bắt đầu trò chơi
game_start_time = pygame.time.get_ticks()
point = Point()
########### Vòng lặp chính #############
running = True
while running:
    screen.fill(WHITE)
    
    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()
    
    # Tính toán thời gian còn lại
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - game_start_time
    remaining_time = max(0, (game_time - elapsed_time) // 1000)  # Đếm ngược theo giây
    
    # Nếu hết giờ, kết thúc trò chơi
    if remaining_time <= 0:
        running = False
        print("Game Over!")
        print(f"Your Score: {point.getPoint()}")
        print(f"Hit Rate: {point.getHitRate():.2%}")
        pygame.quit()
        sys.exit()

    spawn_interval = random.randint(500, 2000)
    
    if len(objs) < num_of_object and current_time - spawn_timer > spawn_interval:
        # Tạo zombie
        objs.append(create_object(objs))
        spawn_timer = current_time
    

    # Cập nhật và vẽ zombie
    objects_to_remove = []
    collided = False
    for obj in objs:
        if isinstance(obj, Zombie):
            if obj.grave_shown:
                grave = Grave(obj.x, obj.y)
                grave.draw(screen)
            if obj.update():
                objects_to_remove.append(obj)
            elif obj.is_rising:
                obj.grave_shown = False
                obj.draw(screen)
            if hammer.check_collision(obj):
                objects_to_remove.append(obj)
                point.hit += 1
                collided = True
        else:
            if obj.update():
                objects_to_remove.append(obj)
            else:
                obj.draw(screen)
            if hammer.check_collision(obj):
                point.hit -= 1
                collided = True
                objects_to_remove.append(obj)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Khi bấm chuột, cây búa nghiêng 125 độ
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.update_rotation(125)
            hammer.mouse_pressed = True
            if not collided:
                point.miss += 1
        # Thả chuột -> Búa trở về trạng thái thẳng đứng
        elif event.type == pygame.MOUSEBUTTONUP:
            hammer.update_rotation(0)
            hammer.mouse_pressed = False
    
    # Vẽ búa theo con trỏ chuột
    hammer.draw_cursor(screen, mouse_pos)
            
    

    # Xóa zombie
    for obj in objects_to_remove:
        if obj in objs:
            objs.remove(obj)
            

    # Hiển thị thời gian và điểm số
    time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    score_text = font.render(f"Score: {point.getPoint()}", True, BLACK)
    miss_text = font.render(f"Score: {point.miss}", True, BLACK)
    hit_rate_text = font.render(f"Hit Rate: {point.getHitRate():.2%}", True, BLACK)
    screen.blit(time_text, (10, 10))
    screen.blit(score_text, (10, 60))
    screen.blit(miss_text, (10, 110))
    screen.blit(hit_rate_text, (10, 160))
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.Clock().tick(60)