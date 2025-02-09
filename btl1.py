import pygame
import sys
import random
import time

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Thiết lập màn hình
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie")
clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
WHITE_BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
HOVER_COLOR = (250, 180, 90)
RED = (255, 0, 0)

# Level
LEVELS = {
    'Easy': 7000,
    'Medium': 5000,
    'Difficult': 4000
}
font = pygame.font.SysFont("comicsansms", 50)
# Load hình ảnh
grave_image = pygame.image.load('./img/grave/grave.webp').convert_alpha()
hammer_image = pygame.image.load('./img/hammer/hammer.webp').convert_alpha()
# zombie_images = [
#     pygame.image.load(f'./img/zombie/zom{i}.jpg').convert_alpha() for i in range(1, 4)
# ]
zombie_images = [
    [pygame.image.load(f'./img/zombie/1_Walk{i}.png').convert_alpha() for i in range(1, 7)],
    [pygame.image.load(f'./img/zombie/2_Walk{i}.png').convert_alpha() for i in range(1, 7)],
    [pygame.image.load(f'./img/zombie/3_Walk{i}.png').convert_alpha() for i in range(1, 7)]
]
zombie_death_images = [
    [pygame.image.load(f'./img/zombie_death/zombie1/Dead{i}.png').convert_alpha() for i in range(1, 9)],
    [pygame.image.load(f'./img/zombie_death/zombie2/Dead{i}.png').convert_alpha() for i in range(1, 9)],
    [pygame.image.load(f'./img/zombie_death/zombie3/Dead{i}.png').convert_alpha() for i in range(1, 9)]
]

explosion = [
    pygame.image.load('./img/explosion.png').convert_alpha(),
    pygame.image.load('./img/explosion2.png').convert_alpha()
]
# font = pygame.font.Font("Chillerz.otf", 50)

##### Hình nền #####
# Load hình nền
background_easy = pygame.image.load("./img/background_easy.jpg").convert()
background_medium = pygame.image.load("./img/background_medium.jpg").convert()
background_difficult = pygame.image.load("./img/background_difficult.jpg").convert()
default_background = pygame.image.load("./img/background_intial.jpg").convert()
background_intial = pygame.image.load("./img/background_intial.jpg").convert()
background_ingame = pygame.image.load("./img/Night.png").convert()


# Resize background phù hợp kích thước màn hình
background_easy = pygame.transform.scale(background_easy, (WIDTH, HEIGHT))
background_medium = pygame.transform.scale(background_medium, (WIDTH, HEIGHT))
background_difficult = pygame.transform.scale(background_difficult, (WIDTH, HEIGHT))
default_background = pygame.transform.scale(default_background, (WIDTH, HEIGHT))
background_intial = pygame.transform.scale(background_intial, (WIDTH, HEIGHT))
background_ingame = pygame.transform.scale(background_ingame, (WIDTH, HEIGHT))


##### Nhạc nền #####
MUSIC = {
    'Easy': "./sound/easy_music.mp3",
    'Medium': "./sound/medium_music.mp3",
    'Difficult': "./sound/difficult_music.mp3"
}
menu_music = "./sound/menu_music.mp3"
instruction_music = "./sound/ins_music.mp3"
result_music = "./sound/res_music.mp3"

# Hàm phát nhạc nền
def play_music(file_path):
    pygame.mixer.music.stop()  # Dừng nhạc hiện tại
    pygame.mixer.music.load(file_path)  # Tải nhạc mới
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)  # Phát lặp vô hạn

# Nạp âm thanh khi đập trúng zombie
hit_zombie = pygame.mixer.Sound('./sound/hit_zombie.wav')  # Đường dẫn tới âm thanh khi đập trúng zombie
hit_zombie.set_volume(0.9)
hit_zombom = pygame.mixer.Sound('./sound/hit_zombom.wav')  # Đường dẫn tới âm thanh khi đập trúng zombie
hit_zombom.set_volume(0.9)


############################ CLASS ############################
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
        self.image_path = ['Zom1.png', 'Zom2.png', 'Zom3.png'] # chỉ dùng để tạo biết loại zombie
        self.zombie_type = random.randint(0, len(self.image_path) - 1)
        self.sprites = zombie_images[self.zombie_type]
        self.sprites_death = zombie_death_images[self.zombie_type]

        self.frame_index = 0
        self.frame_delay = 90  # Chuyển frame mỗi 150ms
        self.last_update = pygame.time.get_ticks()
        
        self.playing_death_animation = False
        self.frame_index_death = 0
        self.last_update_death = pygame.time.get_ticks()

    def draw(self, screen):
        # Cập nhật frame dựa trên thời gian
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_delay:
            self.last_update = current_time
            self.frame_index = (self.frame_index + 1) % len(self.sprites)  # Chuyển frame

        # Lấy hình ảnh theo frame hiện tại
        self.image = self.sprites[self.frame_index]
        
        original_width, original_height = self.image.get_size()

        # Thiết lập kích thước cho từng loại zombie
        if self.zombie_type == 2:
            self.height = 210
        elif self.zombie_type == 1:
            self.height = 175
        else:
            self.height = 161

        self.width = int((self.height / original_height) * original_width)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Cập nhật vị trí và vẽ lên màn hình
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        screen.blit(self.image, self.rect.topleft)

    def draw_death(self, screen):
        # Kiểm tra xem hoạt ảnh đã hoàn thành chưa
        if self.frame_index_death >= len(self.sprites_death):
            return True

        # Vẽ frame hiện tại
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_death > 60:
            self.last_update_death = current_time
            self.frame_index_death += 1

        # Chỉ vẽ nếu vẫn còn frame để hiển thị
        if self.frame_index_death < len(self.sprites_death):
            self.death_image = self.sprites_death[self.frame_index_death]
            original_width, original_height = self.death_image.get_size()
            
            self.height = int((161/403)*original_height)
            self.width = int((self.height / original_height) * original_width)
            
            self.death_image = pygame.transform.scale(self.death_image, (self.width, self.height))
            
            self.rect = self.death_image.get_rect(topleft=(self.x, self.y))
            screen.blit(self.death_image, self.rect.topleft)
        return False

    def update(self):
        global disappear_time
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
        self.image = grave_image
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
        self.image = hammer_image
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
                return self.head_rect.colliderect(zombie_head)
        elif isinstance(obj, Zombie) and obj.is_rising == False:
            return False
        elif isinstance(obj, Bomb):
            return self.mouse_pressed and self.angle != 0 and self.head_rect.colliderect(obj.rect)
        
############### Lớp bomb ################
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, delay):
        super().__init__()
        self.x = x
        self.y = y
        self.start = pygame.time.get_ticks()  # Thời điểm bất đầu
        self.delay = delay
        self.is_rising = False  # Trạng thái trồi lên
        self.dead = False
        self.grave_shown = False
        self.exploding = False  # Kiểm soát trạng thái nổ
        self.explosion_start_time = None  # Lưu thời gian bắt đầu nổ
        self.image_path = ['bomb.png', 'bomb2.png', 'zombom.jpg', 'zombom2.jpg']
        self.img = random.randint(0, len(self.image_path) - 1)
        # Tải ảnh bomb và lưu trữ trong thuộc tính image
        self.image = pygame.image.load('./img/' + self.image_path[self.img]).convert_alpha()  # Hỗ trợ ảnh trong suốt
        if self.img < 2: self.image_explosion = explosion[0]
        else: self.image_explosion = explosion[1]
        
        original_width, original_height = self.image.get_size()
        # Chiều cao mới
        new_height = 161
        # Tính toán chiều rộng mới dựa trên tỉ lệ ban đầu
        new_width = int((new_height / original_height) * original_width)
        # Scale ảnh với chiều rộng và chiều cao mới
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        

    def draw(self, screen):
        # Vẽ hình ảnh lên màn hình
        # Lấy rect từ hình ảnh để định vị
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        screen.blit(self.image, self.rect.topleft)

    def draw_explosion(self, screen):
        self.image = self.image_explosion
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        screen.blit(self.image, self.rect.topleft)
        
    def update(self):
        global disappear_time
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


############### Lớp tính điểm ###############
class Point:
    def __init__(self):
        self.hit = 0
        self.miss = 0
        self.score = 0
        self.life = 3
    
    def getPoint(self):
        return self.score
    
    def getLife(self):
        return self.life

    def getHitRate(self):
        if (self.hit + self.miss == 0 or self.hit < 0): return 0
        return float(self.hit)/(self.hit + self.miss)
    
    def clear(self):
        self.hit = 0
        self.miss = 0
        self.score = 0
        self.life = 3



############################## Hàm hỗ trợ ##############################
# Tạo nhiều zombie và bomb ngẫu nhiên
def create_object(objs):
    while True:
        # Tạo ngẫu nhiên vị trí cho đối tượng
        x = random.randint(0, WIDTH - 100)
        y = random.randint(0, HEIGHT - 205)

        # Tạo rect của đối tượng mới (giả sử kích thước tối đa là 100x200)
        new_rect = pygame.Rect(x, y, 200, 210)
        HUD_rect = pygame.Rect(0, 0, 392, 125)
        # Kiểm tra khoảng cách giữa rect mới và rect của các đối tượng hiện có
        if not new_rect.colliderect(HUD_rect) and all(not new_rect.colliderect(obj.rect) for obj in objs):
            # Xác định loại đối tượng dựa trên tỉ lệ 3:7
            if random.random() < 0.7:  # 70% khả năng xuất hiện Zombie
                zombie = Zombie(x, y, 2900)
                zombie.rect = new_rect  # Gán rect để sử dụng sau
                return zombie
            else:  # 30% khả năng xuất hiện Bomb
                bomb = Bomb(x, y, 2900)
                bomb.rect = new_rect  # Gán rect để sử dụng sau
                return bomb

def reset():
    global selected_level
    global point
    global disappear_time
    disappear_time = 0
    selected_level = None
    point.clear()

########################### Các thuộc tính của game ###########################
selected_level = None
selected_music = None
disappear_time = 0
current_music = None
point = Point()

###################################### Màn hình ########################################
# Xử lý sự kiện chọn level
def menu():
    global selected_level
    global selected_music
    global screen
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
                        selected_music = button.text
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

def play():
    global disappear_time
    global selected_level
    global point
    global screen

    # Ẩn con trỏ chuột mặc định
    pygame.mouse.set_visible(False)
    disappear_time = LEVELS[selected_level]
    current_music = MUSIC[selected_music]
    print(current_music)
    play_music(current_music)

    # Khởi tạo đối tượng búa
    hammer = Hammer()
    
    HUD = pygame.image.load("./img/HUD.png")  
    game_time = 30000
    num_of_object = 5
    objs = []
    spawn_timer = pygame.time.get_ticks()
    # Thời gian bắt đầu trò chơi
    game_start_time = pygame.time.get_ticks()
    ########### Vòng lặp chính #############
    running = True
    while running:
        #screen.fill(WHITE)
        screen.blit(background_ingame, (0,0))

        # HUD
        screen.blit(HUD, (0, 0))

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
        spawn_interval = random.randint(500, 2000)
        
        if len(objs) < num_of_object and current_time - spawn_timer > spawn_interval:
            # Tạo zombie
            objs.append(create_object(objs))
            spawn_timer = current_time
        
        # Cập nhật và vẽ zombie
        objects_to_remove = []

        for obj in objs:
            if obj.grave_shown:
                grave = Grave(obj.x, obj.y)
                grave.draw(screen)
                
            if isinstance(obj, Zombie) and obj.playing_death_animation:  # Nếu zombie đang trong hoạt ảnh chết
                if obj.draw_death(screen):  # Trả về True nếu hoạt ảnh hoàn tất
                    objects_to_remove.append(obj)
                continue
            
            if isinstance(obj, Bomb) and obj.exploding:
                if pygame.time.get_ticks() - obj.explosion_start_time > 200:  # Sau 1 giây thì xóa
                    point.miss += 1
                    point.score -= 5
                    point.life -= 1
                    objects_to_remove.append(obj)
                else:
                    obj.draw_explosion(screen)  # Hiển thị hiệu ứng nổ
            if obj.update():
                objects_to_remove.append(obj)
                if isinstance(obj, Zombie):     # Nếu không kịp đập zombie thường thì sẽ mất mạng + trừ điểm
                    point.life -= 1     
                    point.score -= 5
            elif obj.is_rising:
                obj.grave_shown = False
                obj.draw(screen)

            if isinstance(obj, Zombie):
                if hammer.check_collision(obj):
                    hammer.mouse_pressed = False
                    obj.zombie_type -= 1
                    if obj.zombie_type == -1:
                        obj.playing_death_animation = True
                    else:
                        obj.draw(screen)
                    point.hit += 1
                    point.score += 5
                    hit_zombie.play()  # Phát âm thanh khi trúng zombie
            else:
                if hammer.check_collision(obj):
                    if not obj.exploding:  # Chỉ đặt thời gian nổ nếu chưa được thiết lập
                        obj.explosion_start_time = pygame.time.get_ticks()
                        obj.exploding = True
                        hit_zombom.play()  # Phát âm thanh ngay khi va chạm
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
                
        # Nếu hết mạng thì thua
        if point.life <= 0:
            point.life = 0
            running = False


        # Hiển thị thời gian và điểm số
        status_font = pygame.font.SysFont("comicsansms", 22)
        time_text = status_font.render(f"Time: {remaining_time}s", True, BLACK)
        score_text = status_font.render(f"Score: {point.getPoint()}", True, BLACK)
        lives_text = status_font.render(f"Lives: {point.getLife()}", True, BLACK)
        screen.blit(time_text, (HUD.get_width()/2 - 50, 10))
        screen.blit(score_text, (HUD.get_width()/2 - 50, 50))
        screen.blit(lives_text, (HUD.get_width()/2 - 50, 90))
        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(60)

############# Màn hình kết thúc ###############
def result():
    # Nhạc nền
    play_music(result_music)
    pygame.mouse.set_visible(True)
    bg = pygame.image.load("./img/result_bg.gif")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_image = pygame.image.load("./img/result.png")  

    replay_rect = Button(WIDTH//2 - 180, HEIGHT - 120, 350, 60, "Play Again", BLACK, RED)
    game_mode_text = font.render(f"Game Mode: {selected_level}", True, WHITE)
    score_text = font.render(f"Your Score: {point.getPoint()}", True, WHITE)
    hit_text = font.render(f"Hit: {point.hit}", True, WHITE)
    miss_text = font.render(f"Miss: {point.miss}", True, WHITE)
    hit_rate_text = font.render(f"Hit Rate: {point.getHitRate():.2%}", True, WHITE)

    running = True
    while running:
        screen.blit(bg, (0, 0))  # Hiển thị hình nền
        screen.blit(bg_image, (WIDTH//2 - bg_image.get_width()//2, 0))  # Hiển thị hình nền
        mouse_pos = pygame.mouse.get_pos()

        # Hiệu ứng chữ Game Over
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 150))

        # Hiển thị kết quả game
        screen.blit(game_mode_text, (WIDTH//2 - 200, HEIGHT//2 - 150))
        screen.blit(score_text, (WIDTH//2 - 200, HEIGHT//2 - 100))
        screen.blit(hit_text, (WIDTH//2 - 200, HEIGHT//2 - 50))
        screen.blit(miss_text, (WIDTH//2 - 200, HEIGHT//2))
        screen.blit(hit_rate_text, (WIDTH//2 - 200, HEIGHT//2 + 50))

        replay_rect.handle_hover(mouse_pos)
        replay_rect.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.rect.collidepoint(mouse_pos):
                    running = False
                    reset()
                    pygame.mixer.music.stop()
                    game()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Vẽ button chọn
def draw_button(text, x, y, width, height, button_color, text_color):
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)  # Border_radius làm góc bo tròn
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Vẽ text ra màn hình
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center = (x, y))
    surface.blit(text_obj, text_rect)

# Màn hình hướng dẫn cách chơi
def instruction():
    running = True
    instruction_font = pygame.font.SysFont("comicsansms", 30)
    ins_bg = pygame.image.load("./img/ins_bg2.jpg")
    while running:
        screen.blit(ins_bg, (0, 0))  # Hiển thị hình nền
        draw_text("How to Play:", font, BLACK, screen, WIDTH // 2, HEIGHT // 8)
        draw_text("1. Choose your level: Easy, Medium or Difficult", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 60)
        draw_text("Please remember the higher the level, the faster the speed.", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 2*60)
        draw_text("2. Click mouse on zombie's head to kill zombie.", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 3*60)
        draw_text("There are some zombies that we need to knock multiple times in order to kill.", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 4*60)
        draw_text("If you don't kill a zombie before it disappear or you knock a bomb, you will lose a life.", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 5*60)
        draw_text("A knock on zombies will give you five points. In contrast, a knock on bomb will cost you five point.", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 6*60)
        draw_text("You have three lives. Good luck!", instruction_font, BLACK, screen, WIDTH // 2, HEIGHT // 8 + 7*60)
        draw_text("Press ESC to go back.", font, RED, screen, WIDTH // 2, HEIGHT - 70)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Nhấn ESC để quay lại menu
                    running = False

def game():
    # Nhạc nền
    play_music(instruction_music)
    while True:
        screen.fill(WHITE)
        screen.blit(background_intial, (0, 0))  # Vẽ background

        # Hiển thị nút "Welcome to My Game"
        button_width = 600  # Chiều rộng nút lớn hơn vì đây là nút tiêu đề
        button_height = 80  # Chiều cao nút lớn hơn
        title_y = HEIGHT // 2 - 250  # Căn nút tiêu đề phía trên hai nút còn lại
        draw_button("Zomb or Bomb?", WIDTH // 2 - button_width // 2, title_y, button_width, button_height, GRAY, WHITE)
        
        # Hiển thị nút Play Now và Instruction
        button_width = 300  # Chiều rộng nút tăng để hiển thị chữ rõ hơn
        button_height = 60  # Chiều cao nút
        button_spacing = 30  # Khoảng cách giữa các nút

        draw_button("Play Now", WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - button_spacing, button_width, button_height, RED, WHITE)
        draw_button("Instruction", WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height, BLACK, WHITE)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Kiểm tra vị trí chuột nhấn vào
                if WIDTH // 2 - button_width // 2 < mouse_x < WIDTH // 2 + button_width // 2:
                    if HEIGHT // 2 - button_height - button_spacing < mouse_y < HEIGHT // 2 - button_spacing:
                        play_music(menu_music)
                        menu()
                        play()
                        result()
                    elif HEIGHT // 2 + button_spacing < mouse_y < HEIGHT // 2 + button_spacing + button_height:
                        instruction()  # Gọi màn hình hướng dẫn    

game()