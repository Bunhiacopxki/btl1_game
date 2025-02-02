import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

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
HOVER_COLOR = (250, 180, 90)

# Level
LEVELS = {
    'Easy': 7000,
    'Medium': 5000,
    'Difficult': 4000
}
font = pygame.font.SysFont("comicsansms", 50)

# font = pygame.font.Font("Chillerz.otf", 50)
selected_level = None

################### Hình nền ##############
# Load hình nền
background_easy = pygame.image.load("./img/background_easy.jpg").convert()
background_medium = pygame.image.load("./img/background_medium.jpg").convert()
background_difficult = pygame.image.load("./img/background_difficult.jpg").convert()
default_background = pygame.image.load("./img/default_background.jpg").convert()

# Resize background phù hợp kích thước màn hình
background_easy = pygame.transform.scale(background_easy, (WIDTH, HEIGHT))
background_medium = pygame.transform.scale(background_medium, (WIDTH, HEIGHT))
background_difficult = pygame.transform.scale(background_difficult, (WIDTH, HEIGHT))
default_background = pygame.transform.scale(default_background, (WIDTH, HEIGHT))

################# Nhạc nền ################
# Nạp nhạc nền
pygame.mixer.music.load('./sound/background_music.mp3')  # Đường dẫn tới nhạc nền
pygame.mixer.music.set_volume(0.05)  # Nhạc nền ở mức 80%
pygame.mixer.music.play(-1, 0.0)  # Phát nhạc nền, vòng lặp vô hạn

# Nạp âm thanh khi đập trúng zombie
hit_zombie = pygame.mixer.Sound('./sound/hit_zombie.wav')  # Đường dẫn tới âm thanh khi đập trúng zombie
hit_zombie.set_volume(0.9)
hit_zombom = pygame.mixer.Sound('./sound/hit_zombom.wav')  # Đường dẫn tới âm thanh khi đập trúng zombie
hit_zombom.set_volume(0.9)
# Tạo các nút chế độ chơi
class Button:
    def __init__(self, x, y, width, height, text, base_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color  # Màu hiện tại
        self.is_hovered = False  # Trạng thái hover

    def draw(self, screen):
        # Vẽ nút
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=15)
        # Đổ bóng (shadow)
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, BLACK, shadow_rect, border_radius=15)

        # Vẽ text
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_hover(self, mouse_pos):
        # Cập nhật trạng thái hover
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.base_color

# Tạo danh sách nút
buttons = [
    Button(600, 300, 200, 50, "Easy", GREEN, HOVER_COLOR),
    Button(600, 400, 200, 50, "Medium", GRAY, HOVER_COLOR),
    Button(600, 500, 200, 50, "Difficult", BLACK, HOVER_COLOR),
]


# In Level ra màn hình
# def draw_menu():
#     screen.fill(WHITE)
#     title_text = font.render("Welcome to my game", True, BLACK)
#     bar_text = font.render("Choose your level", True, BLACK)
#     easy_text = font.render("Easy", True, BLACK)
#     medium_text = font.render("Medium", True, BLACK)
#     difficult_text = font.render("Difficult", True, BLACK)
#     title_rect = title_text.get_rect(center = (WIDTH//2, HEIGHT//2 - 250))
#     bar_rect = bar_text.get_rect(center = (WIDTH//2, HEIGHT//2 - 200))
#     easy_rect = easy_text.get_rect(center = (WIDTH//2, HEIGHT//2 - 100))
#     medium_rect = medium_text.get_rect(center = (WIDTH//2, HEIGHT//2))
#     difficult_rect = difficult_text.get_rect(center = (WIDTH//2, HEIGHT//2 + 100))
#     screen.blit(title_text, title_rect)  # blit: Vẽ text vào vị trí rect
#     screen.blit(bar_text, bar_rect)
#     screen.blit(easy_text, easy_rect)
#     screen.blit(medium_text, medium_rect)
#     screen.blit(difficult_text, difficult_rect)
#     pygame.display.flip()
#     return easy_rect, medium_rect, difficult_rect

# Xử lý sự kiện chọn level
current_background = default_background  # Hình nền mặc định
choosing_level = True
while choosing_level:
    #screen.blit(background_image, (0, 0))  # Vẽ hình nền

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_hovered:
                    selected_level = button.text
                    choosing_level = False
                    print(f"Chế độ chơi: {button.text}")
                    
    # kiểm tra trạng thái hover của các nút
    for button in buttons:
        button.handle_hover(mouse_pos)

    # Thay đổi background dựa trên trạng thái hover
    if buttons[0].is_hovered:
        current_background = background_easy
    elif buttons[1].is_hovered:
        current_background = background_medium
    elif buttons[2].is_hovered:
        current_background = background_difficult
    else:
        current_background = default_background

    # Vẽ màn hình
    screen.blit(current_background, (0, 0))  # Vẽ background
    # Vẽ các nút
    for button in buttons:
        button.draw(screen)

    pygame.display.update()  # Cập nhật màn hình
    pygame.time.Clock().tick(60)

# choosing_level = True
# while choosing_level:
#     easy_rect, medium_rect, difficult_rect = draw_menu()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = event.pos
#             if easy_rect.collidepoint(x, y):
#                 selected_level = 'easy'
#             elif medium_rect.collidepoint(x, y):
#                 selected_level = 'medium'
#             elif difficult_rect.collidepoint(x, y):
#                 selected_level = 'difficult'
#             if selected_level:
#                 choosing_level = False

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
        self.grave_shown = False
        self.image_path = ['zom1.jpg', 'zom2.jpg', 'zom3.jpg']
        self.zombie_type = random.randint(0, len(self.image_path) - 1)

    def draw(self, screen):
        # Tải ảnh bomb và lưu trữ trong thuộc tính image
        self.image = pygame.image.load('./img/zombie/' + self.image_path[self.zombie_type]).convert_alpha()  # Hỗ trợ ảnh trong suốt
        original_width, original_height = self.image.get_size()
        # Chiều cao mới
        if self.zombie_type == 2:
            self.height = 210
        elif self.zombie_type == 1:
            self.height = 175
        else:
            self.height = 161
        # Tính toán chiều rộng mới dựa trên tỉ lệ ban đầu
        self.width = int((self.height / original_height) * original_width)
        # Scale ảnh với chiều rộng và chiều cao mới
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # Lấy rect từ hình ảnh để định vị
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        # Vẽ hình ảnh lên màn hình
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Hiển thị ngôi mộ trước zombie
        if not self.grave_shown and current_time - self.start > self.delay - 1000:
            self.grave_shown = True
        
        # Kích hoạt hiệu ứng trồi lên sau khi hết delay
        if not self.is_rising and current_time - self.start > self.delay:
            self.is_rising = True

        #  Xuất hiện 5s rồi die
        if self.is_rising and current_time - self.start > disappear_time:
            self.dead = True

        return self.dead
       
# Định nghĩa và thiết kế lớp Grave    
class Grave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('./img/grave/grave.webp').convert_alpha()
        original_width, original_height = self.image.get_size()
        # Chiều cao mới
        new_height = 150
        # Tính toán chiều rộng mới dựa trên tỉ lệ ban đầu
        new_width = int((new_height / original_height) * original_width)
        # Scale ảnh với chiều rộng và chiều cao mới
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Hammer:
    def __init__(self):
        self.image = pygame.image.load('./img/hammer/hammer.webp').convert_alpha()
        original_width, original_height = self.image.get_size()
        # Chiều cao mới
        new_height = 100
        # Tính toán chiều rộng mới dựa trên tỉ lệ ban đầu
        new_width = int((new_height / original_height) * original_width)
        # Scale ảnh với chiều rộng và chiều cao mới
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rotated_image = self.image  # Ảnh mặc định
        self.angle = 0  # Góc quay mặc định
        self.mouse_pressed = False      

    def update_rotation(self, angle):
        # Cập nhật góc quay của búa
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    # Vẽ búa tại vị trí con trỏ chuột
    def draw_cursor(self, screen, pos):
        rotated_rect = self.rotated_image.get_rect(center = pos)
        screen.blit(self.rotated_image, rotated_rect.topleft)
        self.head_rect = rotated_rect
        
    def check_collision(self, obj):
        if isinstance(obj, Zombie) and obj.is_rising:
            if self.mouse_pressed and self.angle != 0:
                head_size = [0.1, 0.2, 0.3]
                zombie_head = pygame.Rect(obj.x, obj.y, obj.width, obj.height * head_size[obj.zombie_type])
                self.mouse_pressed = False
                return self.head_rect.colliderect(zombie_head)
        elif isinstance(obj, Zombie) and obj.is_rising == False:
            return False
        elif isinstance(obj, Bomb):
            return self.mouse_pressed and self.angle != 0 and self.head_rect.colliderect(obj.rect)
        
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
                obj.zombie_type -= 1
                if obj.zombie_type == -1:
                    objects_to_remove.append(obj)
                else:
                    obj.draw(screen)
                point.hit += 1
                
                hit_zombie.play()  # Phát âm thanh khi trúng zombie
        else:
            if obj.update():
                objects_to_remove.append(obj)
            else:
                obj.draw(screen)
            if hammer.check_collision(obj):
                point.hit -= 1
                objects_to_remove.append(obj)
                hit_zombom.play()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Khi bấm chuột, cây búa nghiêng 125 độ
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.update_rotation(125)
            hammer.mouse_pressed = True
            # Chỉ tăng điểm miss nếu không có va chạm
            collided = any(hammer.check_collision(obj) for obj in objs)
            collided_bomb = any(isinstance(obj, Bomb) and hammer.check_collision(obj) for obj in objs)
            if not collided or collided_bomb:
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
    score_text = font.render(f"Hit: {point.getPoint()}", True, BLACK)
    miss_text = font.render(f"Miss: {point.miss}", True, BLACK)
    hit_rate_text = font.render(f"Hit Rate: {point.getHitRate():.2%}", True, BLACK)
    screen.blit(time_text, (10, 10))
    screen.blit(score_text, (10, 60))
    screen.blit(miss_text, (10, 110))
    screen.blit(hit_rate_text, (10, 160))
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.Clock().tick(60)