import pygame
import random

pygame.init()

running = True


screen = pygame.display.set_mode((800, 600))
cell_image = pygame.image.load('./cell.jpg').convert()
cell_image = pygame.transform.scale(cell_image, (cell_image.get_width() / 8, cell_image.get_height() / 8))
bacteria_img = pygame.image.load('cell.jpg').convert()
bacteria_img = pygame.transform.scale(bacteria_img, (bacteria_img.get_width() / 8, bacteria_img.get_height() / 8))

clock = pygame.time.Clock()

BACT_SPAWN_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(BACT_SPAWN_EVENT, 5000)

moving_right = False
moving_left = False
x = 0
delta_time = 0.1

bacteria_y = []
bacteria_x = []

while running:
    screen.fill((0, 0, 0))
    screen.blit(cell_image, (x, 400))
    
    hitbox = pygame.Rect(x, 400, cell_image.get_width(), cell_image.get_height())


    
    # for a in bacteria_x:
    #     if bacteria_y < 600:
    #         screen.blit(bacteria_img, (a, bacteria_y))

    for i in range(len(bacteria_y)):
        bacteria_y[i] += 50 * delta_time
        draw_bact = True
        target = pygame.Rect(bacteria_x[i], bacteria_y[i], bacteria_img.get_width(), bacteria_img.get_height())
        if hitbox.colliderect(target):
            draw_bact = False
            
        if(bacteria_y[i] < 600 and draw_bact ):
            screen.blit(bacteria_img, (bacteria_x[i], bacteria_y[i]))




        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False
        if event.type == BACT_SPAWN_EVENT:
            bacteria_x.append(random.randint(1, 800))
            bacteria_y.append(0)

    if moving_right == True:
        x += 200 * delta_time

    if moving_left == True:
        x -= 200 * delta_time


    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    
    pygame.display.flip()




pygame.quit()

