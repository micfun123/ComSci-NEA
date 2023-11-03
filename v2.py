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

# Text box properties
TEXT_BOX_WIDTH = 200
TEXT_BOX_HEIGHT = 40
TEXT_BOX_COLOR = (200, 200, 200)
TEXT_BOX_ACTIVE_COLOR = (150, 150, 150)  # Color for active input box
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 30

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Bouncing with Damping")

# Initialize the ball
ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
ball_speed_x, ball_speed_y = INITIAL_SPEED_X, 0

# Initialize the font
font = pygame.font.Font(None, FONT_SIZE)

# Input box for damping factor
input_box = pygame.Rect(10, 10, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)
damping_factor = 0.9
input_text = "Damping: {}".format(damping_factor)
active_input = False


def draw_speed_text(surface, speed):
    text_box = pygame.Surface((120, 40))
    text_box.fill(TEXT_BOX_COLOR)
    speed_text = font.render("Speed: {:.2f}".format(abs(speed)), True, TEXT_COLOR)
    surface.blit(text_box, (10, 60))
    surface.blit(speed_text, (20, 70))


def draw_input_box():
    color = TEXT_BOX_ACTIVE_COLOR if active_input else TEXT_BOX_COLOR
    pygame.draw.rect(screen, color, input_box, border_radius=6)
    # clear format the text in the input box
    input_surface = font.render(input_text, True, TEXT_COLOR)
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active_input = not active_input
            else:
                active_input = False
        if event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    damping_factor = float(input_text.split(":")[-1])
                    active_input = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        if damping_factor > 1:
            damping_factor = 1
            input_text = "Damping: {}".format(damping_factor)

        elif damping_factor < 0:
            damping_factor = 0
            input_text = "Damping: {}".format(damping_factor)

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

    # Draw the ball and the screen
    screen.fill(SCREEN_COLOR)
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

    # Display speed in the text box
    draw_speed_text(screen, ball_speed_x)

    # Draw the input box
    draw_input_box()

    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
