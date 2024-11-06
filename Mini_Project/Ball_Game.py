import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Paddle and Ball
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10
paddle_speed = 8
x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
dx, dy = 0, 0

# Power-Ups
power_up_active = False
power_up_timer = 0
power_up_types = ['widen', 'extra_life', 'score_multiplier']
power_up = None
power_up_rect = None

# Game State
score = 0
ball_launched = False
game_over = False
lives = 3

# Font and Backgrounds
font = pygame.font.Font(None, 36)
backgrounds = {
    "countryside": pygame.image.load("countryside.png").convert(),
    "city": pygame.image.load("city.png").convert(),
    "underwater": pygame.image.load("underwater.png").convert()
}
background_theme = "countryside"

# Power-Up Effects
def activate_power_up(power_up_type):
    global paddle_x, PADDLE_WIDTH, score
    if power_up_type == "widen":
        PADDLE_WIDTH = 150
    elif power_up_type == "extra_life":
        lives += 1
    elif power_up_type == "score_multiplier":
        score += 5

# Generate Random Power-Up
def generate_power_up():
    global power_up, power_up_rect
    power_up = random.choice(power_up_types)
    power_up_rect = pygame.Rect(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 200), 30, 30)

# Draw Power-Up
def draw_power_up():
    if power_up == "widen":
        color = (0, 255, 0)
    elif power_up == "extra_life":
        color = (255, 0, 0)
    elif power_up == "score_multiplier":
        color = (0, 0, 255)
    pygame.draw.ellipse(screen, color, power_up_rect)

# Animated Text Boxes
def draw_animated_text_box(text, pos):
    box_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=pos)
    box_rect = text_rect.inflate(20, 20)
    pygame.draw.rect(screen, box_color, box_rect, border_radius=8)
    screen.blit(text_surface, text_rect)

# Game Loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not ball_launched and not game_over:
            dx, dy = random.choice([-5, 5]), -5
            ball_launched = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x = max(0, paddle_x - paddle_speed)
    if keys[pygame.K_RIGHT]:
        paddle_x = min(WIDTH - PADDLE_WIDTH, paddle_x + paddle_speed)

    if not game_over:
        if ball_launched:
            x += dx
            y += dy

        if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
            dx = -dx

        if y - RADIUS <= 0:
            dy = -dy

        if dy > 0 and y + RADIUS >= paddle_y and paddle_x <= x <= paddle_x + PADDLE_WIDTH:
            dy = -dy
            score += 1
            generate_power_up()

        if y + RADIUS >= HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                ball_launched = False
                x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS

        # Check for power-up collection
        if power_up_rect and paddle_y <= power_up_rect.y <= paddle_y + PADDLE_HEIGHT and \
           paddle_x <= power_up_rect.x <= paddle_x + PADDLE_WIDTH:
            activate_power_up(power_up)
            power_up = None
            power_up_rect = None

        # Background Cycle
        background_theme = "countryside" if score < 5 else "city" if score < 10 else "underwater"
        screen.blit(backgrounds[background_theme], (0, 0))

        # Draw paddle, ball, and power-ups
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, WHITE, (x, y), RADIUS)
        if power_up:
            draw_power_up()

    # Animated Text Boxes
    draw_animated_text_box(f"Score: {score}", (WIDTH // 2, 30))
    draw_animated_text_box(f"Lives: {lives}", (WIDTH - 70, 30))
    if game_over:
        draw_animated_text_box("Game Over! Press R to Restart", (WIDTH // 2, HEIGHT // 2))

    if keys[pygame.K_r] and game_over:
        x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
        dx, dy = 0, 0
        score = 0
        ball_launched = False
        game_over = False
        lives = 3
        PADDLE_WIDTH = 100

    pygame.display.flip()
    clock.tick(60)