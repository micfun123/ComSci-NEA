import pygame
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_COLOR = (255, 255, 255)

# Ball properties
BALL_RADIUS = 20
BALL_COLOR = (0, 0, 255)
INITIAL_SPEED_X = 5
MAX_DAMPING_FACTOR = 0.95

# Damping bar properties
DAMPING_BAR_WIDTH = 20
DAMPING_BAR_HEIGHT = 400
DAMPING_BAR_COLOR = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Bouncing with Damping")

# Initialize the ball
ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
ball_speed_x, ball_speed_y = INITIAL_SPEED_X, 0

# Initialize the damping bar
damping_bar_rect = pygame.Rect(50, 100, DAMPING_BAR_WIDTH, DAMPING_BAR_HEIGHT)
damping_factor = 1.0

# Initialize the font
font = pygame.font.Font(None, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the ball's position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collisions with the screen edges
    if ball_x + BALL_RADIUS >= SCREEN_WIDTH:
        ball_x = SCREEN_WIDTH - BALL_RADIUS
        ball_speed_x *= -damping_factor

    if ball_x - BALL_RADIUS <= 0:
        ball_x = BALL_RADIUS
        ball_speed_x *= -damping_factor

    if ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
        ball_y = SCREEN_HEIGHT - BALL_RADIUS
        ball_speed_y *= -damping_factor

    if ball_y - BALL_RADIUS <= 0:
        ball_y = BALL_RADIUS
        ball_speed_y *= -damping_factor

    # Check for mouse interaction with the damping bar
    if pygame.mouse.get_pressed()[0]:
        if damping_bar_rect.collidepoint(pygame.mouse.get_pos()):
            mouse_y = pygame.mouse.get_pos()[1]
            normalized_mouse_y = max(0, min(mouse_y - damping_bar_rect.y, DAMPING_BAR_HEIGHT))
            damping_factor = 1 - normalized_mouse_y / DAMPING_BAR_HEIGHT
            damping_factor = max(1 - MAX_DAMPING_FACTOR, min(damping_factor, 1.0))

    # Draw the ball, the screen, and the damping bar
    screen.fill(SCREEN_COLOR)
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)
    pygame.draw.rect(screen, DAMPING_BAR_COLOR, damping_bar_rect)

    # Display speed and damping in the top left corner
    speed_text = font.render("Speed: {:.2f}".format(abs(ball_speed_x)), True, (0, 0, 0))
    damping_text = font.render("Damping: {:.2f}".format(1 - damping_factor), True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))
    screen.blit(damping_text, (10, 40))

    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
