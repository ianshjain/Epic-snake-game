import pygame
import random
import sys

# INIT
pygame.init()

# DISPLAY SETTINGS
width, height = 600, 400
block_size = 20
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Epic Snake Game")
clock = pygame.time.Clock()

# COLORS
color_bg = (30, 30, 30)
color_grid = (40, 40, 40)
color_snake_head = (255, 0, 70)
color_snake_body = (200, 0, 100)
color_food = (0, 162, 255)
color_font = (255, 255, 255)

# FONTS
score_font = pygame.font.SysFont('Consolas', 20)
title_font = pygame.font.SysFont('Arial', 40)

# DRAW GRID
def draw_grid():
    for x in range(0, width, block_size):
        pygame.draw.line(game_display, color_grid, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(game_display, color_grid, (0, y), (width, y))

# DRAW SNAKE
def draw_snake(snake_blocks):
    for i, block in enumerate(snake_blocks):
        color = color_snake_head if i == len(snake_blocks) - 1 else color_snake_body
        pygame.draw.rect(game_display, color, [block[0], block[1], block_size, block_size], border_radius=8)

# DRAW FOOD
def draw_food(x, y):
    pygame.draw.circle(game_display, color_food, (x + block_size // 2, y + block_size // 2), block_size // 2 - 2)

# SHOW SCORE
def draw_score(score):
    text = score_font.render(f"Score: {score}", True, color_font)
    game_display.blit(text, [10, 10])

# START SCREEN
def start_screen():
    game_display.fill(color_bg)
    title = title_font.render("Epic Snake Game", True, color_font)
    prompt = score_font.render("Press ANY arrow key to start...", True, color_font)
    game_display.blit(title, [width // 2 - title.get_width() // 2, height // 3])
    game_display.blit(prompt, [width // 2 - prompt.get_width() // 2, height // 2])
    pygame.display.update()

    # Wait for arrow key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    waiting = False

# MAIN GAME
def game_loop():
    x, y = width // 2, height // 2
    dx, dy = 0, 0
    snake = [[x, y]]
    length = 3
    speed = 10

    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    running = True
    start_screen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -block_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, block_size
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -block_size, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = block_size, 0

        if dx == 0 and dy == 0:
            continue  # Wait for movement

        x += dx
        y += dy

        # Wall collision
        if x < 0 or x >= width or y < 0 or y >= height:
            break

        # Update snake
        snake.append([x, y])
        if len(snake) > length:
            del snake[0]

        # Self-collision
        if snake[-1] in snake[:-1]:
            break

        # Food collision
        if x == food_x and y == food_y:
            length += 1
            speed += 0.3
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

        # Draw everything
        game_display.fill(color_bg)
        draw_grid()
        draw_snake(snake)
        draw_food(food_x, food_y)
        draw_score(length - 3)
        pygame.display.update()
        clock.tick(int(speed))

    # Game over
    game_over_screen(length - 3)

# GAME OVER SCREEN
def game_over_screen(score):
    while True:
        game_display.fill(color_bg)
        over = title_font.render("GAME OVER", True, color_font)
        final_score = score_font.render(f"Final Score: {score}", True, color_font)
        prompt = score_font.render("Press SPACE to play again or ESC to quit", True, color_font)
        game_display.blit(over, [width // 2 - over.get_width() // 2, height // 3])
        game_display.blit(final_score, [width // 2 - final_score.get_width() // 2, height // 2.2])
        game_display.blit(prompt, [width // 2 - prompt.get_width() // 2, height // 1.8])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# START GAME
game_loop()
