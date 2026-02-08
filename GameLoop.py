import pygame
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cell vs Bacteria - With Score")
clock = pygame.time.Clock()

# --- Fonts ---
# We need two fonts: one big for Game Over, one small for Score
game_over_font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)

# --- Load Background Image ---
try:
    background = pygame.image.load("bloody-arm.png").convert()
    background = pygame.transform.scale(background, (800, 600))
except FileNotFoundError:
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 0))

# --- Define the Floor Rectangle ---
floor_rect = pygame.Rect(0, 590, 800, 10)


# --- 1. Define the Bacteria (Enemy) ---
class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(1, 5):
            try:
                filename = f"bact{i}.png"
                img = pygame.image.load(filename).convert_alpha()
                img = pygame.transform.scale(img, (80, 80))
                self.images.append(img)
            except FileNotFoundError:
                pass

        if len(self.images) == 0:
            surf = pygame.Surface((30, 30))
            surf.fill((255, 0, 0))
            self.images.append(surf)

        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(0, 800 - self.rect.width)
        self.rect.y = -100
        self.speed_y = random.randrange(3, 4)

    def update(self):
        self.rect.y += self.speed_y
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.images):
            self.current_frame = 0
        self.image = self.images[int(self.current_frame)]
        self.mask = pygame.mask.from_surface(self.image)


# --- 2. Define the Cell (Player) ---
class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("cell.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
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
            self.speed_x = -10
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 10


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 590:
            self.rect.bottom = 590


# --- 3. Setup Groups ---
all_sprites = pygame.sprite.Group()
bacteria_group = pygame.sprite.Group()
player = Cell()
all_sprites.add(player)


def spawn_bacteria():
    b = Bacteria()
    all_sprites.add(b)
    bacteria_group.add(b)


# Game Variables
SPAWN_DELAY = 60
spawn_timer = 0
score = 0  # <--- NEW: Score variable
running = True
game_over = False

# --- 4. Game Loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        spawn_timer += 1
        if spawn_timer >= SPAWN_DELAY:
            spawn_bacteria()
            spawn_timer = 0

        all_sprites.update()

        # Check for bacteria collision (EATING)
        hits = pygame.sprite.spritecollide(player, bacteria_group, True, pygame.sprite.collide_mask)

        # <--- NEW: Increase Score ---
        for hit in hits:
            score += 1
            # print(f"Score: {score}") # Debug print

        # Check Floor Collision (GAME OVER)
        for bacteria in bacteria_group:
            if bacteria.rect.colliderect(floor_rect):
                game_over = True

                # --- DRAWING ---
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), floor_rect)

    # <--- NEW: Draw the Score ---
    # render("Text", Anti-alias, Color)
    score_text = score_font.render(f"Bacteria Eaten: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Draw at top-left corner

    if game_over:
        # Draw "GAME OVER"
        text = game_over_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 300))

        # Draw Final Score
        final_score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(400, 350))

        # Overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(text, text_rect)
        screen.blit(final_score_text, final_score_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()