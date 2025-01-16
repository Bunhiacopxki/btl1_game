import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
WIDTH, HEIGHT = 800, 600
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
font = pygame.font.Font("Chillerz.otf", 50)
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
        
    def check_collision(self, zombie):
        if zombie.is_rising:
            return self.mouse_pressed and self.angle != 0 and self.head_rect.colliderect(zombie.head_rect)
        return False
        
# Ẩn con trỏ chuột mặc định
pygame.mouse.set_visible(False)

# Khởi tạo đối tượng búa
hammer = Hammer()
                      
# Tạo nhiều zombie ngẫu nhiên
def create_zombies(zombies):
    while True:
        x = random.randint(0, WIDTH - 100)
        y = random.randint(0, HEIGHT - 205)
        if all(abs(x - zombie.x) > 100 for zombie in zombies):
            return Zombie(x, y, 2900)

num_of_zombies = 5
zombies = []
spawn_timer = pygame.time.get_ticks()

# Vòng lặp chính
running = True
while running:
    screen.fill(WHITE)
    
    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()
    
    spawn_interval = random.randint(500, 2000)
    current_time = pygame.time.get_ticks()
    if len(zombies) < num_of_zombies and current_time - spawn_timer > spawn_interval:
        # Tạo zombie
        zombies.append(create_zombies(zombies))
        spawn_timer = current_time
    
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Khi bấm chuột, cây búa nghiêng 125 độ
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.update_rotation(125)
            hammer.mouse_pressed = True
        # Thả chuột -> Búa trở về trạng thái thẳng đứng
        elif event.type == pygame.MOUSEBUTTONUP:
            hammer.update_rotation(0)
            hammer.mouse_pressed = False
            
    # Vẽ búa theo con trỏ chuột
    hammer.draw_cursor(screen, mouse_pos)

    # Cập nhật và vẽ zombie
    zombies_to_remove = []
    for zombie in zombies:
        if zombie.grave_shown:
            grave = Grave(zombie.x, zombie.y)
            grave.draw(screen)
        if zombie.update():
            zombies_to_remove.append(zombie)
        elif zombie.is_rising:
            zombie.grave_shown = False
            zombie.draw(screen)
        if hammer.check_collision(zombie):
            zombies_to_remove.append(zombie)
            
    # Xóa zombie
    for zombie in zombies_to_remove:
        if zombie in zombies:
            zombies.remove(zombie)
            
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.Clock().tick(60)