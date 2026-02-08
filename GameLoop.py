import pygame
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cell vs Bacteria - Animated")
clock = pygame.time.Clock()

# --- Load Background Image ---
try:
    background = pygame.image.load("bloody-arm.png").convert()
    background = pygame.transform.scale(background, (800, 600))
except FileNotFoundError:
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 0))


# --- 1. Define the Bacteria (Enemy) ---
class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # --- ANIMATION STEP 1: Load all images into a list ---
        self.images = []
        # We assume your files are named bact1.png, bact2.png, etc.
        for i in range(1, 5):
            try:
                filename = f"bact{i}.png"  # This creates "bact1.png", "bact2.png"...
                img = pygame.image.load(filename).convert_alpha()
                img = pygame.transform.scale(img, (100, 100))
                self.images.append(img)
            except FileNotFoundError:
                print(f"Could not load {filename}")

        # Fallback if no images found
        if len(self.images) == 0:
            surf = pygame.Surface((30, 30))
            surf.fill((255, 0, 0))
            self.images.append(surf)

        # --- ANIMATION STEP 2: Setup Counters ---
        self.current_frame = 0  # Start at the first image
        self.animation_speed = 0.2  # How fast to cycle (lower = slower)

        # Set the initial image
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Standard Movement Variables
        self.rect.x = random.randrange(0, 800 - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(3, 8)

    def update(self):
        # 1. Move Down
        self.rect.y += self.speed_y

        # --- ANIMATION STEP 3: Cycle the Images ---
        # Increase the frame counter
        self.current_frame += self.animation_speed

        # If the number exceeds our list length, loop back to 0
        if self.current_frame >= len(self.images):
            self.current_frame = 0

        # Update the actual image shown
        # We use int() because indices must be whole numbers (0, 1, 2...)
        self.image = self.images[int(self.current_frame)]

        # IMPORTANT: If your animation frames are different shapes,
        # you must update the mask every frame so collision stays accurate.
        self.mask = pygame.mask.from_surface(self.image)

        # 2. Kill if off screen
        if self.rect.top > 600:
            self.kill()


# --- 2. Define the Cell (Player) ---
class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("cell.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (200, 200))
        except FileNotFoundError:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.centerx = 400
        self.rect.bottom = 580
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_a]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


# --- 3. Setup Groups ---
all_sprites = pygame.sprite.Group()
bacteria_group = pygame.sprite.Group()

player = Cell()
all_sprites.add(player)


def spawn_bacteria():
    b = Bacteria()
    all_sprites.add(b)
    bacteria_group.add(b)


for i in range(8):
    spawn_bacteria()

# --- 4. Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    if len(bacteria_group) < 8:
        spawn_bacteria()

    # Collision Check (using masks)
    hits = pygame.sprite.spritecollide(player, bacteria_group, True, pygame.sprite.collide_mask)

    for hit in hits:
        spawn_bacteria()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()