import pygame,math,time,random


pygame.init()
screen = pygame.display.set_mode((750,500))
pygame.display.set_caption("Treasure Quests")

score = 0
gravity = 0.09
velocity_y = 0
velocity_x = 0
Acceleration = 0.5
max_speed = 5
Friction = 0.1
start = pygame.time.get_ticks()

#color
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
brown = (150,75,0)
white = (255,255,255)


#character
man_standing = pygame.image.load("essent/standing.png")
man_standing = pygame.transform.scale(man_standing, (50,100))
man_walking = pygame.image.load("essent/walking.png")
man_walking = pygame.transform.scale(man_walking, (50,100))
man_running = pygame.image.load("essent/runing.png")
man_running = pygame.transform.scale(man_running, (85,100))
man_jump = pygame.image.load("essent/jump.png")
man_jump = pygame.transform.scale(man_jump, (60,100))
man_dash = pygame.image.load("essent/dash.png")
man_dash = pygame.transform.scale(man_dash, (85,100))
man_image = man_standing
man_rect = man_image.get_rect()
man_rect.centerx = screen.width // 2
man_rect.centery = screen.height // 2
square = pygame.image.load("essent/glass block.png")
square = pygame.transform.scale(square,(1500,100))
square_rect = square.get_rect()
square_rect.centerx = 625
square_rect.centery = 455
trophy = pygame.image.load("essent/trophy.png")
trophy = pygame.transform.scale(trophy,(50,50))
trophy_rect = trophy.get_rect()
trophy_rect.centerx = screen.width // 2
trophy_rect.centery = screen.height // 2

floor_rect = pygame.Rect(0,0,450,1500)

#Fps
fps = 120
clock = pygame.time.Clock()

#screen color
screen.fill(white)

#label
sys_text_crate = pygame.font.SysFont("arial", 20)

#sound
collect_sound = pygame.mixer.Sound("essent/coin.wav")
collect_sound.set_volume(0.05)

#display
runtime = True
while runtime:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = False
    #physics
    man_rect.x += velocity_x
    moving = False
    velocity_y += gravity
    man_rect.y += velocity_y
    on_ground = man_rect.colliderect(square_rect)
    second = (pygame.time.get_ticks() - start) // 1000
    keys = pygame.key.get_pressed()
    if velocity_x == 0:
        man_image = man_standing
    if velocity_x > max_speed:
        velocity_x = max_speed
    if velocity_x == max_speed:
        man_image = man_running
    if velocity_x < -max_speed:
        velocity_x = -max_speed
    if man_rect.right > screen.width:
        man_rect.right = screen.width
    if man_rect.left < 0:
        man_rect.left = 0
    #sprite
    if moving:
        man_image = man_standing
    else:
        if on_ground:
            if velocity_x == 0:
                man_image = man_standing
            elif velocity_x == max_speed:
                man_image = man_running
            elif velocity_x == -max_speed:
                man_image = pygame.transform.flip(man_running, True, False)
            elif velocity_x > 0:
                man_image = man_walking
            elif velocity_x < 0:
                man_image = pygame.transform.flip(man_walking, True, False)
        elif velocity_x == 0:
            man_image = man_jump
    #moving in x
    if keys[pygame.K_q] and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
        velocity_x -= 5
    if keys[pygame.K_q] and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
        velocity_x += 5
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and man_rect.left > 0:
        velocity_x -= Acceleration
        moving = True
        man_image = pygame.transform.flip(man_running, True, False)
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and man_rect.right < screen.width:
        velocity_x += Acceleration
        moving = True
        man_image = man_running
    if not moving:
        if velocity_x > 0:
                velocity_x = max(0, velocity_x - Friction)
        elif velocity_x < 0:
             velocity_x = min(0, velocity_x + Friction)
    #moving in  y
    if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and man_rect.top > 0 and man_rect.colliderect(square_rect) :
        velocity_y -= 5
        man_rect.y -= 5
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and man_rect.bottom < 415:
        man_rect.y += 5
        man_image = man_jump
    #screen sitting
    screen.fill(white)
    score_text = sys_text_crate.render(f"score: {score}",True,black)
    time_text = sys_text_crate.render(f"time: {second}",True,black)
    howto_text = sys_text_crate.render(f"W,A,S,D for Move, A,D+Q for Dash",True,black)
    velocity_text = sys_text_crate.render(f"velocity ===> moving:{round(velocity_x, 4)}m/s falling:{round(velocity_y, 3)}m/s",True,black)
    #collabh
    if man_rect.colliderect(trophy_rect):
        trophy_rect.x = random.randint(0, screen.width-50)
        trophy_rect.y = random.randint(screen.height-300, screen.height-120)
        score += 1
        collect_sound.play()
    if man_rect.colliderect(square_rect):
        velocity_y = 0
    screen.blit(howto_text, (10, 25))
    screen.blit(time_text, (10, 50))
    screen.blit(score_text, (10, 75))
    screen.blit(velocity_text, (10, 100))
    screen.blit(man_image, man_rect)
    screen.blit(square, square_rect)
    screen.blit(trophy, trophy_rect)
    clock.tick(fps)
pygame.quit()
