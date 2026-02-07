import pygame

pygame.init()

running = True


screen = pygame.display.set_mode((800, 600))
cell_image = pygame.image.load('./cell.jpg').convert()
cell_image = pygame.transform.scale(cell_image, (cell_image.get_width() / 4, cell_image.get_height() / 4))

moving_right = False
moving_left = False
x = 0
while running:
    screen.fill((0, 0, 0))
    screen.blit(cell_image, (x, 200))

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
    if moving_right == True:
        x+=1

    if moving_left == True:
        x-=1
    pygame.display.flip()




pygame.quit()

