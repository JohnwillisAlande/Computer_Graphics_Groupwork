import pygame  # Import Pygame library for game development
import sys     # Import sys for system functions, such as exiting the game
import random  # Import random for generating random values
import os

# Initialize Pygame library
pygame.init()
pygame.mixer.init()  # Initialize Pygame mixer for music and sounds

# Constants for game window dimensions and colors
WIDTH, HEIGHT = 600, 400          # Screen width and height
RADIUS = 20                        # Ball radius
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10  # Paddle dimensions
WHITE = (255, 255, 255)            # RGB color for white
BLACK = (0, 0, 0)                  # RGB color for black

# Create the game display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Ball Game')  # Set window title

# Initial position for paddle and its speed
paddle_x = (WIDTH - PADDLE_WIDTH) // 2  # Center paddle horizontally
paddle_y = HEIGHT - PADDLE_HEIGHT - 10  # Position paddle near bottom of screen
paddle_speed = 8                        # Paddle movement speed

# Initial position and velocity for the ball
x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS  # Start above paddle center
dx, dy = 0, 0  # Ball starts stationary

# Score and game state flags
score = 0            # Player's score
ball_launched = False  # Tracks if the ball has been launched
game_over = False      # Tracks if the game is over

# Set font for displaying text on the screen
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Random initial background and target colors
background_color = random.choices(range(256), k=3)  # RGB for gradient background
target_color = random.choices(range(256), k=3)      # Target color for smooth transition
ball_color = (0, 0, 255)  # Blue ball

# Leaderboard file
LEADERBOARD_FILE = "leaderboard.txt"

# Ensure the leaderboard file exists
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        pass  # Create an empty file

# Music and sound effects
background_music = "background_music.mp3"  # Replace with your background music file
collision_sound = pygame.mixer.Sound("collision.wav")  # Replace with collision sound file
power_up_sound = pygame.mixer.Sound("power_up.mp3")  # Replace with power-up sound file
game_over_sound = pygame.mixer.Sound("game_over.wav")  # Replace with game over sound file

# Set sound volumes
collision_sound.set_volume(0.8)
power_up_sound.set_volume(0.8)
game_over_sound.set_volume(0.8)

# Start background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Music and sound toggle
music_enabled = True
sound_enabled = True


# Start Menu
menu_options = ['New Game', 'High Scores', 'Skill Mode', 'Exit']
skill_levels = {
    'Beginner': {'paddle_width': 120, 'ball_speed': 4},
    'Intermediate': {'paddle_width': 100, 'ball_speed': 6},
    'Expert': {'paddle_width': 80, 'ball_speed': 8},
}
# Default skill level
current_skill = 'Beginner'

MENU_HIGHLIGHT = (100, 100, 255)
MENU_GRAY = (200, 200, 200)

current_skill_level = "Beginner"
PADDLE_WIDTH = skill_levels[current_skill_level]["paddle_width"]
BALL_SPEED = skill_levels[current_skill_level]["ball_speed"]

def display_start_menu():
    # Variables for menu state
    selected_option = 0
    in_menu = True
    in_skill_selection = False
    selected_skill = 0  # Default skill level index

    while in_menu:
        # Clear the screen for the current frame
        draw_gradient_background(background_color, BLACK)

        # Display the game title
        title_text = font.render('Welcome to Ball Paddle Game', True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Display menu options
        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else MENU_GRAY
            option_text = font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 150 + i * 60))

        # Update display
        pygame.display.flip()

        # Display skill level options if in skill selection
        if in_skill_selection:
            for i, skill in enumerate(skill_levels):
                color = MENU_HIGHLIGHT if i == selected_skill else MENU_GRAY
                skill_text = small_font.render(skill, True, color)
                screen.blit(skill_text, (WIDTH // 2 - skill_text.get_width() // 2, 350 + i * 40))

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if in_skill_selection:
                    # Navigate skill levels
                    if event.key == pygame.K_UP:
                        selected_skill = (selected_skill - 1) % len(skill_levels)
                    elif event.key == pygame.K_DOWN:
                        selected_skill = (selected_skill + 1) % len(skill_levels)
                    elif event.key == pygame.K_RETURN:
                        print(f"Skill Level Selected: {skill_levels[selected_skill]}")
                        in_skill_selection = False  # Exit skill selection
                else:
                    # Navigate main menu
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        # Handle menu options
                        if selected_option == 0:  # New Game
                            return True  # Exit menu and start the game
                        elif selected_option == 1:  # High Scores
                            display_leaderboard_screen()
                        elif selected_option == 2:  # Skill Level
                            display_skill_level()
                        elif selected_option == 3:  # Exit
                            pygame.quit()
                            sys.exit()


def set_skill_level(level):
    global PADDLE_WIDTH, BALL_SPEED

    PADDLE_WIDTH = skill_levels[level]['paddle_width']
    BALL_SPEED = skill_levels[level]['ball_speed']


def display_skill_level():
    selected_skill = 0  # Default skill level index
    in_skill_selection = True
    skill_names = list(skill_levels.keys())

    while in_skill_selection:
        # Clear the screen
        screen.fill(BLACK)

        # Display title
        title_text = font.render('Select Skill Level', True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Display skill levels
        for i, skill in enumerate(skill_names):
            color = MENU_HIGHLIGHT if i == selected_skill else MENU_GRAY
            skill_text = font.render(skill, True, color)
            screen.blit(skill_text, (WIDTH // 2 - skill_text.get_width() // 2, 150 + i * 60))

        # Update display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_skill = (selected_skill - 1) % len(skill_levels)
                elif event.key == pygame.K_DOWN:
                    selected_skill = (selected_skill + 1) % len(skill_levels)
                elif event.key == pygame.K_RETURN:
                    # Set selected skill level
                    selected_level = skill_names[selected_skill]
                    set_skill_level(selected_level)
                    return  # Exit skill selection and return to the main menu


def display_leaderboard_screen():
    in_leaderboard = True

    while in_leaderboard:
        # Clear the screen
        screen.fill(BLACK)

        # Display title
        title_text = font.render('Leaderboard', True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Fetch and display leaderboard
        leaderboard = get_leaderboard()
        for i, score in enumerate(leaderboard):
            score_text = small_font.render(f"{i + 1}. {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 150 + i * 40))

        # Instruction to return to main menu
        return_text = small_font.render("Press ENTER to return to the Main Menu", True, MENU_GRAY)
        screen.blit(return_text, (WIDTH // 2 - return_text.get_width() // 2, HEIGHT - 50))

        # Update display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # Exit leaderboard and return to the main menu


# Smoothly transition colors for background
def smooth_color_transition(current, target, speed=1):
    return tuple(min(255, max(0, current[i] + (speed if current[i] < target[i] else -speed))) for i in range(3))

# Draw gradient background between two colors
def draw_gradient_background(color1, color2):
    for i in range(HEIGHT):
        ratio = i / HEIGHT  # Gradual color blending ratio
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))  # Draw a horizontal line for each row

# Realistic shadow for the ball
def draw_colored_shadow(ball_x, ball_y, ball_radius, paddle_y):
    """Draw a realistic shadow below the ball."""
    shadow_distance = max(0, paddle_y - ball_y)
    shadow_opacity = max(50, min(150, 200 - shadow_distance))
    shadow_color = (0, 0, 0, shadow_opacity)
    shadow_surface = pygame.Surface((ball_radius * 4, ball_radius * 2), pygame.SRCALPHA)
    shadow_width = ball_radius * 2
    shadow_height = ball_radius // 2
    pygame.draw.ellipse(
        shadow_surface,
        shadow_color,
        (ball_radius - shadow_width // 2, ball_radius, shadow_width, shadow_height),
    )
    shadow_x = ball_x - ball_radius * 2
    shadow_y = paddle_y + PADDLE_HEIGHT
    screen.blit(shadow_surface, (shadow_x, shadow_y))


# Shaded ball for 3D effect
def draw_shaded_ball(ball_x, ball_y, ball_radius, ball_color):
    """Draw the ball with gradient shading for a 3D effect."""
    surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
    for i in range(ball_radius, 0, -1):
        color_value = int((ball_radius - i) * 255 / ball_radius)
        gradient_color = (
            min(255, ball_color[0] + color_value),
            min(255, ball_color[1] + color_value),
            min(255, ball_color[2] + color_value),
            255,
        )
        pygame.draw.circle(surface, gradient_color, (ball_radius, ball_radius), i)
    screen.blit(surface, (ball_x - ball_radius, ball_y - ball_radius))


# Leaderboard functions
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
    leaderboard_title = font.render("Leaderboard:", True, WHITE)
    screen.blit(leaderboard_title, (WIDTH // 2 - leaderboard_title.get_width() // 2, HEIGHT // 2 - 40))
    leaderboard = get_leaderboard()
    for i, score in enumerate(leaderboard):
        score_text = small_font.render(f"{i + 1}. {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + i * 30))

# Display instructions before the game starts
def display_instructions():
    screen.fill(BLACK)
    title = font.render("Bouncing Ball Game", True, WHITE)
    instructions = [
        "Press Left/Right Arrow Keys to Move Paddle",
        "Press Any Key to Launch the Ball",
        "Press 'M' to Toggle Background Music",
        "Press 'S' to Toggle Sound Effects",
        "Avoid Missing the Ball!",
        "Press Any Key to Start..."
    ]
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    for i, text in enumerate(instructions):
        line = font.render(text, True, WHITE)
        screen.blit(line, (WIDTH // 2 - line.get_width() // 2, HEIGHT // 2 + i * 30))
    pygame.display.flip()
    wait_for_key()


def display_game_over_menu():
    selected_option = 0  # 0 for Restart, 1 for Main Menu
    options = ["Restart", "Main Menu"]

    while True:

        draw_gradient_background(background_color, BLACK)  # Clear screen with black background

        # Display game over text
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        # Display menu options
        for i, option in enumerate(options):
            color = WHITE if i == selected_option else MENU_GRAY
            option_text = font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 50))

        pygame.display.flip()  # Refresh the screen

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Enter key
                    return selected_option

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

# Initialise skill level
set_skill_level(current_skill)

# Main game loop
clock = pygame.time.Clock()

if not display_start_menu():
    sys.exit()
display_instructions()
while True:
    # Handle events, such as quitting the game or pressing keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Close the game window
            sys.exit()     # Exit the program
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Toggle music
                music_enabled = not music_enabled
                if music_enabled:
                    pygame.mixer.music.unpause()  # Resume music
                else:
                    pygame.mixer.music.pause()  # Pause music
            elif event.key == pygame.K_s:  # Toggle sound
                sound_enabled = not sound_enabled
            elif event.key == pygame.K_r and game_over:  # Restart game
                # Reset ball and paddle properties
                x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
                dx = random.choice([-BALL_SPEED, BALL_SPEED])
                dy = -BALL_SPEED
                score = 0
                ball_launched = False
                game_over = False
                background_color = random.choices(range(256), k=3)
                target_color = random.choices(range(256), k=3)
                if music_enabled:
                    pygame.mixer.music.play(-1)  # Restart music
            elif not ball_launched and not game_over:
                dx = random.choice([-BALL_SPEED, BALL_SPEED])
                dy = -BALL_SPEED  # Adjust speed dynamically
                ball_launched = True  # Launch the ball

    # Paddle movement controls
    keys = pygame.key.get_pressed()  # Check pressed keys
    if keys[pygame.K_LEFT]:          # Move paddle left if within screen bounds
        paddle_x = max(0, paddle_x - paddle_speed)
    if keys[pygame.K_RIGHT]:         # Move paddle right if within screen bounds
        paddle_x = min(WIDTH - PADDLE_WIDTH, paddle_x + paddle_speed)

    # Only update game state if the game is not over
    if not game_over:
        if ball_launched:
            x += dx  # Update ball's x-coordinate
            y += dy  # Update ball's y-coordinate

        # Ball collision with left and right walls
        if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
            dx = -dx  # Reverse ball's horizontal direction
            if sound_enabled:
                collision_sound.play()  # Play collision sound
            target_color = random.choices(range(256), k=3)  # Change background target color

        # Ball collision with the top wall
        if y - RADIUS <= 0:
            dy = -dy  # Reverse ball's vertical direction
            if sound_enabled:
                collision_sound.play()  # Play collision sound
            target_color = random.choices(range(256), k=3)  # Change background target color

        # Ball collision with the paddle
        if dy > 0 and y + RADIUS >= paddle_y and paddle_x <= x <= paddle_x + PADDLE_WIDTH:
            dy = -dy  # Reverse ball's vertical direction
            score += 1  # Increase score
            if sound_enabled:
                power_up_sound.play()  # Play power-up sound
            target_color = random.choices(range(256), k=3)  # Change background target color

        # Game over if ball falls below the paddle
        if y + RADIUS >= HEIGHT:
            game_over = True  # Set game state to over
            dy = 0  # Stop ball movement
            if sound_enabled:
                game_over_sound.play()  # Play game over sound
            pygame.mixer.music.stop()  # Stop background music immediately
            update_leaderboard(score)

    # Update gradient background color
    background_color = smooth_color_transition(background_color, target_color, speed=2)
    if background_color == target_color:
        target_color = random.choices(range(256), k=3)  # Update target color if transition complete
    draw_gradient_background(background_color, BLACK)

    # Draw paddle and ball
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Paddle
    if not ball_launched:
        x = paddle_x + PADDLE_WIDTH // 2  # Position ball above center of paddle
        y = paddle_y - RADIUS
    pygame.draw.circle(screen, WHITE, (x, y), RADIUS)  # Ball

    # Display score and instructions
    if not game_over:
        draw_colored_shadow(x, y, RADIUS, paddle_y)
        draw_shaded_ball(x, y, RADIUS, ball_color)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        option = display_game_over_menu()
        if option == 0:  # Restart
            # Reset game variables
            x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
            dx = random.choice([-BALL_SPEED, BALL_SPEED])
            dy = -BALL_SPEED
            score = 0
            ball_launched = False
            game_over = False
            background_color = random.choices(range(256), k=3)
            target_color = random.choices(range(256), k=3)
            if music_enabled:
                pygame.mixer.music.play(-1)  # Restart music
        elif option == 1:  # Main Menu
            if not display_start_menu():  # Return to main menu
                sys.exit()
            # Reset variables for a new game session
            x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
            dx = random.choice([-BALL_SPEED, BALL_SPEED])
            dy = -BALL_SPEED
            score = 0
            ball_launched = False
            game_over = False
            background_color = random.choices(range(256), k=3)
            target_color = random.choices(range(256), k=3)

    # Refresh the display
    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS