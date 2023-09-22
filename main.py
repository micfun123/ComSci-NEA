import sys
import math
import random
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

colours_list = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown"]

# screen
pygame.init()
screendata = pygame.display.Info()
SCREEN_WIDTH = screendata.current_w - 50
SCREEN_HEIGHT = screendata.current_h - 50


# Create a section for controlling initial settings
control_section = pygame.Rect(SCREEN_WIDTH - 250, 0, 250, SCREEN_HEIGHT)
control_bg_color = (200, 200, 200)

sim_with = SCREEN_WIDTH - 250
sim_height = SCREEN_HEIGHT


# init

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Billard Balls Collision")


# Define a Vector2 class for 2D vector operations.
class Vector2:
    # Initialize a vector with x and y coordinates.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Set the current vector's coordinates to match another vector 'v'.
    def set(self, v) -> None:
        self.x = v.x
        self.y = v.y

    # Add another vector 'v' to the current vector.
    def add(self, v) -> None:
        self.x += v.x
        self.y += v.y

    # Subtract a scalar value 'v' from both x and y coordinates.
    def sub(self, v) -> None:
        self.x -= v
        self.y -= v

    # Multiply both x and y coordinates by a scalar 'n'.
    def mult(self, n) -> None:
        self.x *= n
        self.y *= n

    # Divide both x and y coordinates by a scalar 'n'.
    def div(self, n) -> None:
        self.x /= n
        self.y /= n

    # Calculate the magnitude (length) of the vector.
    def mag(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    # Calculate the dot product of the vector with another vector 'v'.
    def dot(self, v) -> float:
        if v is None:
            print("Error: 'v' is None")
            return 0  # Return a default value or raise an exception
        return self.x * v.x + self.y * v.y

    # Calculate the cross product of the vector with another vector 'v'.
    def cross(self, v) -> float:
        return self.x * v.y - self.y * v.x

    # Normalize the vector (make it a unit vector with a magnitude of 1).
    def normalize(self) -> None:
        mag = self.mag()
        if mag != 0:
            return Vector2(self.x / mag, self.y / mag)
        else:
            return Vector2(0, 0)  # Return a zero vector if the magnitude is zero

    # Limit the magnitude of the vector to a maximum value.
    def limit(self, max_magnitude) -> None:
        if self.mag() > max_magnitude:
            self.normalize()
            self.mult(max_magnitude)

    # Calculate the Euclidean distance between two vectors 'v1' and 'v2'.
    @staticmethod
    def distance(v1, v2) -> float:
        dx = v1.x - v2.x
        dy = v1.y - v2.y
        return math.sqrt(dx * dx + dy * dy)

    # Create a copy of the vector.
    def copy(self) -> "Vector2":
        return Vector2(self.x, self.y)

    # Create a clone of the vector 'v'.
    @classmethod
    def clone(cls, v) -> "Vector2":
        return cls(v.x, v.y)

    # Provide a string representation of the vector.
    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Ball:
    def __init__(self, x, y, mass, color, velocity=Vector2(0, 0)):
        self.pos = Vector2(x, y)
        self.mass = mass
        # Calculate the radius based on the mass (you can adjust the scaling factor as needed)
        self.radius = int(math.sqrt(mass) * 20)
        self.color = color
        self.velocity = velocity

    def move(self):
        self.pos.add(self.velocity)

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius
        )

    def check_boundary_collision(self, simWidth, simHeight):
        if (
            self.pos.x - self.radius < 0 or self.pos.x + self.radius > simWidth
        ):  # left or right wall
            self.velocity.x *= -1  # reverse x velocity
        if (
            self.pos.y - self.radius < 0 or self.pos.y + self.radius > simHeight
        ):  # ceiling or floor collition
            self.velocity.y *= -1  # reverse y velocity

    def check_ball_collision(self, other_ball):
        # Calculate the vector between the centers of the two balls
        distance_vector = Vector2(
            other_ball.pos.x - self.pos.x, other_ball.pos.y - self.pos.y
        )

        # Calculate the distance between the centers of the two balls
        distance = distance_vector.mag()

        # Check if there is a collision
        if distance < self.radius + other_ball.radius:
            # Calculate the collision normal
            collision_normal = distance_vector.normalize()

            # Calculate the relative velocity
            relative_velocity = Vector2(
                other_ball.velocity.x - self.velocity.x,
                other_ball.velocity.y - self.velocity.y,
            )

            # Calculate the relative velocity in the direction of the collision
            relative_speed = relative_velocity.dot(collision_normal)

            # Check if the balls are moving toward each other
            if relative_speed < 0:
                # Calculate the impulse scalar
                impulse_scalar = -(1 + damping_factor) * relative_speed
                impulse_scalar /= 1 / self.mass + 1 / other_ball.mass

                # Apply impulses
                self.velocity.x -= impulse_scalar / self.mass * collision_normal.x
                self.velocity.y -= impulse_scalar / self.mass * collision_normal.y
                other_ball.velocity.x += (
                    impulse_scalar / other_ball.mass * collision_normal.x
                )
                other_ball.velocity.y += (
                    impulse_scalar / other_ball.mass * collision_normal.y
                )

                # Move the balls apart
                overlap = 0.5 * (distance - self.radius - other_ball.radius + 1)
                self.pos.x -= overlap * collision_normal.x
                self.pos.y -= overlap * collision_normal.y
                other_ball.pos.x += overlap * collision_normal.x
                other_ball.pos.y += overlap * collision_normal.y


# Create instances of Ball
balls = []
for i in range(7):
    balls.append(
        Ball(
            random.randint(100, sim_with - 100),
            random.randint(100, SCREEN_HEIGHT - 100),
            random.randint(1, 10),
            THECOLORS[colours_list[random.randint(0, 7)]],
            Vector2(random.randint(-5, 5), random.randint(-5, 5)),
        )
    )


# Set the initial damping factor
damping_factor = 0.6


# Function to update the damping factor
def set_damping(factor):
    global damping_factor
    damping_factor = factor


# Function to prompt user for a new damping factor
def update_damping():
    try:
        damping = float(input("Enter damping factor (0.0 to 1.0): "))
        if 0.0 <= damping <= 1.0:
            set_damping(damping)
        else:
            print("Damping factor should be between 0.0 and 1.0.")
    except ValueError:
        print("Invalid input. Please enter a number between 0.0 and 1.0.")


font = pygame.font.SysFont("Arial", 20)


# Function to draw a text input box
def draw_text_input_box(x, y, width, height, text, active):
    color = (4, 240, 20) if active else (100, 100, 100)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + 5, y + 5))
    # text for damping factor
    text = font.render(
        "Press D to change Damping: " + str(damping_factor), True, (0, 0, 0)
    )
    screen.blit(text, (SCREEN_WIDTH - 220, 60))


# Initialize the damping factor input
input_box = pygame.Rect(SCREEN_WIDTH - 220, 20, 200, 30)
input_text = ""
input_active = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_d:
                input_active = not input_active
            if input_active:
                if event.key == K_RETURN:
                    try:
                        damping = float(input_text)
                        if 0.0 <= damping <= 1.0:
                            set_damping(damping)
                            input_text = ""
                    except ValueError:
                        print(
                            "Invalid input. Please enter a number between 0.0 and 1.0."
                        )
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the control section background
    pygame.draw.rect(screen, control_bg_color, control_section)
    # Move and draw the balls
    for ball in balls:
        ball.move()
        ball.draw(screen)
        # text for velocity rounded to 2 decimal places
        font = pygame.font.SysFont("Arial", 15)
        text = font.render(
            "Velocity: " + str(round(ball.velocity.mag(), 2)), True, (0, 0, 0)
        )
        screen.blit(text, (ball.pos.x - 30, ball.pos.y - 30))
        # text for mass
        text = font.render("Mass: " + str(ball.mass), True, (0, 0, 0))
        screen.blit(text, (ball.pos.x - 30, ball.pos.y - 15))

    # Check for boundary collisions
    for ball in balls:
        ball.check_boundary_collision(sim_with, SCREEN_HEIGHT)

    # Check for ball-ball collisions
    for ball in balls:
        for other_ball in balls:
            if ball != other_ball:
                ball.check_ball_collision(other_ball)

    # Draw the damping factor input box
    draw_text_input_box(
        input_box.x,
        input_box.y,
        input_box.width,
        input_box.height,
        input_text,
        input_active,
    )

    pygame.display.flip()
    pygame.time.Clock().tick(60)
    print(damping_factor)
