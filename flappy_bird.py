import pygame
from random import randint  # Import hàm random

pygame.init()

WIDTH, HEIGHT = 400, 600

# Tô màu nên, khung nền đầu tiên
screen = pygame.display.set_mode((400,600))
pygame.display.set_caption('Flappy Bird')


running = True

# Khai báo màu cơ bản
GREEN = (0,200,0)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)

# Giữ cho chương trình chạy 60pfs
clock = pygame.time.Clock()

# Khai báo ống
TUBE_WIDTH = 50
TUBE_VELOCITY = 3   # Khai báo Velocity

TUBE_GAP = 150

# Khai báo chiều dài
tube1_x = 600
tube2_x = 800
tube3_x = 1000

# Khai báo chiều cao, dạn random
tube1_height = randint(100,400)
tube2_height = randint(100,400)
tube3_height = randint(100,400)

# Khai báo, tạo chim
BIRD_X = 50
bird_y = 400
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
bird_drop_velocity = 0
GRAVITY = 0.5           # Mục đích : tăng dần đều, tạo độ rơi

# Tính điểm, tạo font hiển thị điểm số
score = 0
font = pygame.font.SysFont('sans', 20)

# Load hình ảnh. Bird/Backgound/Sand
background_image = pygame.image.load("background-day.png")
background_image = pygame.transform.scale(background_image, (WIDTH,HEIGHT)) # Scale ảnh cho vừa khung hình
bird_image = pygame.image.load("redbird.png")  
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH,BIRD_HEIGHT))
sand_image = pygame.image.load("base.png")
sand_image = pygame.transform.scale(sand_image, (400,50))

# Khai báo biến cho ống, mục đích tính điểm. Khi qua 1 ống sẽ báo là False
tube1_pass = False
tube2_pass = False
tube3_pass = False

pausing = False

while running:
    clock.tick(60)
    screen.fill(GREEN)

    # Hiển thị ảnh background
    screen.blit(background_image, (0,0))


    #Draw tube top
    tube1_rect = pygame.draw.rect(screen, BLUE, (tube1_x, 0, TUBE_WIDTH, tube1_height))
    tube2_rect = pygame.draw.rect(screen, BLUE, (tube2_x, 0, TUBE_WIDTH, tube2_height))
    tube3_rect = pygame.draw.rect(screen, BLUE, (tube3_x, 0, TUBE_WIDTH, tube3_height))

    #Draw tube bottom, inverse
    tube1_rect_inv = pygame.draw.rect(screen, BLUE, (tube1_x, tube1_height+TUBE_GAP, TUBE_WIDTH, HEIGHT-tube1_height-TUBE_GAP))
    tube2_rect_inv = pygame.draw.rect(screen, BLUE, (tube2_x, tube2_height+TUBE_GAP, TUBE_WIDTH, HEIGHT-tube2_height-TUBE_GAP))
    tube3_rect_inv = pygame.draw.rect(screen, BLUE, (tube3_x, tube3_height+TUBE_GAP, TUBE_WIDTH, HEIGHT-tube3_height-TUBE_GAP))

    # Move tube to the left
    tube1_x = tube1_x - TUBE_VELOCITY
    tube2_x = tube2_x - TUBE_VELOCITY
    tube3_x = tube3_x - TUBE_VELOCITY

    # Draw sand
    #sand_rect = pygame.draw.rect(screen, YELLOW,(0,550,400,50))
    sand_rect = screen.blit(sand_image, (0,550,400,50))

    # Draw bird
    # bird_rect = pygame.draw.rect(screen, RED, (BIRD_X,bird_y,BIRD_WIDTH, BIRD_HEIGHT))
    bird_rect = screen.blit(bird_image, (BIRD_X,bird_y,BIRD_WIDTH, BIRD_HEIGHT))

    # Bird falls. Tạo chim rơi, với độ rơi tăng dần đều, biến Gravity [0.5] --> bird_y sẽ tăng dần đều
    # Ví du: Gravity = 0.5 - Giây 1 biến y sẽ rơi 0.5, giây 2 sẽ rơi 1, giây 3 sẽ rơi 1.5. cứ thế tăng dần đều
    bird_y += bird_drop_velocity        # bird_y = bird_y + bird_drop_velocity
    bird_drop_velocity += GRAVITY       # bird_drop_velocity = bird_drop_velocity + gravity


    # generate new tubes/Tao ong moi
    if tube1_x < -TUBE_WIDTH:               # Nếu x nhỏ hơn chiều ngang, tương đương ống 1 sẽ trở về bên phải, 550
        tube1_x = 550
        tube1_height = randint(100,400) # Chiều cao sẽ là 1 số random
        tube1_pass = False              # sau khi qua phải, ống sẽ được đánh là sai
    if tube2_x < -TUBE_WIDTH:
        tube2_x = 550
        tube2_height = randint(100,400)
        tube2_pass = False              # Điều kiện này sẽ giúp cho tính điểm lặp lại. Tạo mới 1 tube là tạo thêm 1 điểm
    if tube3_x < -TUBE_WIDTH:
        tube3_x = 550
        tube3_height = randint(100,400)
        tube3_pass = False

    # Draw score._ Vẽ điểm số
    score_txt = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_txt, (5,5))

    # Tính điểm khi đi qua 3 cột
    if tube1_x + TUBE_WIDTH <= BIRD_X and tube1_pass == False:          # Khi qua 1 cột gồm trục x < chiều ngang cột và đánh sai theo biển trên
        score += 1                                                      # khi đó điểm số sẽ cộng 1
        tube1_pass = True                                               # Sau khi cộng 1 sẽ đổi thành Đúng, khi đổi điều kiện thành đúng thì sẽ cộng điểm 1 lần, không cộng thành nhiều lần
    if tube2_x + TUBE_WIDTH <= BIRD_X and tube2_pass == False:
        score += 1
        tube2_pass = True                                               # Tương tự, khi thành đúng sẽ không chạy lại if, qua vòng lặp While mới chạy lại thành False
    if tube3_x + TUBE_WIDTH <= BIRD_X and tube3_pass == False:
        score += 1
        tube3_pass = True

    # Check collision. kiểm tra xem các ống và chim có chạm nhau không
    # if bird_rect.colliderect(tube1_rect):       # Tương đương == True
    #     TUBE_VELOCITY = 0
    # if bird_rect.colliderect(tube2_rect):       # Tương đương == True
    #     TUBE_VELOCITY = 0
    # if bird_rect.colliderect(tube3_rect):       # Tương đương == True
    #     TUBE_VELOCITY = 0

    # Kiểm tra check collision. Cách 2. Check từng ống trong list, tránh lặp lại code
    for tube in [tube1_rect,tube2_rect,tube3_rect,tube1_rect_inv,tube2_rect_inv,tube3_rect_inv,sand_rect]:
        if bird_rect.colliderect(tube):
            pausing = True
            TUBE_VELOCITY = 0
            bird_drop_velocity = 0
            game_over_txt = font.render("Game Over, score: " + str(score),True, BLACK)
            screen.blit(game_over_txt, (200,300))
            press_space_txt = font.render("Press Space to Continue" ,True, BLACK)
            screen.blit(press_space_txt, (150,350))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # Khi nhấn nút Quit sẽ thoát chương trình
            running = False
        if event.type == pygame.KEYDOWN:        # Khi nhấn núi spacpace, nó sẽ đặt điều kiệu cho chim
            if event.key == pygame.K_SPACE:     # Câu lệnh bắt buộc
                # reset space pace
                if pausing: 
                    bird_y = 400
                    TUBE_VELOCITY = 3
                    tube1_x = 600
                    tube2_x = 800
                    tube3_x = 1000
                    score = 0
                    pausing = False                
                bird_drop_velocity = 0          # Trả lại vị trí của velocity = 0
                bird_drop_velocity -= 8        # nếu nhấn nhiều lần sẽ cho chim bay lên

        
    pygame.display.flip()

pygame.quit()