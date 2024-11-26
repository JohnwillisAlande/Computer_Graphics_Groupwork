import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Ball Game')

# Initial paddle position
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10
paddle_speed = 8

# Initial ball position and velocity
x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
dx, dy = 0, 0  # Ball starts stationary

# Score and game state
score = 0
ball_launched = False
game_over = False

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Initial colors
background_color = random.choices(range(256), k=3)
target_color = random.choices(range(256), k=3)
ball_color = (0, 0, 255)  # Blue ball

# Leaderboard file
LEADERBOARD_FILE = "leaderboard.txt"

# Ensure the leaderboard file exists
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        pass  # Create an empty file


def smooth_color_transition(current, target, speed=1):
    """Smoothly transition between two colors."""
    return tuple(
        min(255, max(0, current[i] + (speed if current[i] < target[i] else -speed)))
        for i in range(3)
    )


def draw_gradient_background(color1, color2):
    """Draw a gradient background transitioning between two colors."""
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))


def draw_reflection(ball_x, ball_y, ball_radius):
    """Draw a semi-transparent reflection of the ball."""
    reflection_color = (200, 200, 255, 128)  # Light blue reflection
    reflection_y = HEIGHT + (HEIGHT - ball_y)  # Mirrored below screen
    pygame.draw.circle(screen, reflection_color, (ball_x, reflection_y), ball_radius)


def draw_colored_shadow(ball_x, ball_y, ball_radius, ball_color):
    """Draw a shadow for the ball with a dimmed version of its color."""
    shadow_color = tuple(max(0, c // 2) for c in ball_color)  # Dimmed ball color
    shadow_width = ball_radius * 2
    shadow_height = ball_radius // 2
    shadow_x = ball_x - shadow_width // 2
    shadow_y = ball_y + ball_radius
    pygame.draw.ellipse(screen, shadow_color, (shadow_x, shadow_y, shadow_width, shadow_height))


def draw_shaded_ball(ball_x, ball_y, ball_radius, ball_color):
    """Draw the ball with a gradient shading effect."""
    surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
    for i in range(ball_radius, 0, -1):
        color_value = 255 - int((ball_radius - i) * 255 / ball_radius)
        gradient_color = (0, 0, color_value, 255)  # Gradient blue
        pygame.draw.circle(surface, gradient_color, (ball_radius, ball_radius), i)
    screen.blit(surface, (ball_x - ball_radius, ball_y - ball_radius))


def get_leaderboard():
    """Read leaderboard from file and return as a sorted list of scores."""
    with open(LEADERBOARD_FILE, "r") as f:
        scores = [int(line.strip()) for line in f if line.strip().isdigit()]
    return sorted(scores, reverse=True)[:5]  # Top 5 scores


def update_leaderboard(new_score):
    """Update leaderboard with a new score."""
    scores = get_leaderboard()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:5]  # Keep top 5 scores
    with open(LEADERBOARD_FILE, "w") as f:
        f.writelines(f"{score}\n" for score in scores)


def display_leaderboard():
    """Display leaderboard on the screen."""
    leaderboard = get_leaderboard()
    leaderboard_title = font.render("Leaderboard:", True, WHITE)
    screen.blit(leaderboard_title, (WIDTH // 2 - leaderboard_title.get_width() // 2, HEIGHT // 4))
    for i, score in enumerate(leaderboard):
        score_text = small_font.render(f"{i + 1}. {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4 + 30 * (i + 1)))


def display_score(score):
    """Display the current score during gameplay."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Main loop
clock = pygame.time.Clock()
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not ball_launched and not game_over:
            dx, dy = random.choice([-5, 5]), -5
            ball_launched = True

    # Paddle control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x = max(0, paddle_x - paddle_speed)
    if keys[pygame.K_RIGHT]:
        paddle_x = min(WIDTH - PADDLE_WIDTH, paddle_x + paddle_speed)

    # Update game state if not over
    if not game_over:
        if ball_launched:
            x += dx
            y += dy

        # Ball collision with walls
        if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
            dx = -dx
            target_color = random.choices(range(256), k=3)

        # Ball collision with the top
        if y - RADIUS <= 0:
            dy = -dy
            target_color = random.choices(range(256), k=3)

        # Ball collision with paddle
        if dy > 0 and y + RADIUS >= paddle_y and paddle_x <= x <= paddle_x + PADDLE_WIDTH:
            dy = -dy
            score += 1
            target_color = random.choices(range(256), k=3)

        # Game over if ball falls below paddle
        if y + RADIUS >= HEIGHT:
            game_over = True
            dy = 0  # Stop ball movement
            update_leaderboard(score)  # Save score to leaderboard

    # Gradient background update
    background_color = smooth_color_transition(background_color, target_color, speed=2)
    if background_color == target_color:
        target_color = random.choices(range(256), k=3)

    screen.fill(BLACK)
    draw_gradient_background(background_color, BLACK)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    if not game_over:
        draw_colored_shadow(x, y, RADIUS, ball_color)
        draw_reflection(x, y, RADIUS)
        draw_shaded_ball(x, y, RADIUS, ball_color)  # Ball with gradient shading
        display_score(score)  # Display current score
    else:
        # Display leaderboard and game over message
        display_leaderboard()
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 + 150))

        # Restart game on pressing 'R'
        if keys[pygame.K_r]:
            x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
            dx, dy = 0, 0
            score = 0
            ball_launched = False
            game_over = False
            background_color = random.choices(range(256), k=3)
            target_color = random.choices(range(256), k=3)

    # Update display and cap frame rate
    pygame.display.flip()
    clock.tick(60)