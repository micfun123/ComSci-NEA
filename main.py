#py games billard balls collision

import sys
import math
import random
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

colours_list = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white"]



#screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

simMinWidth = 2
cscale = SCREEN_WIDTH / simMinWidth, SCREEN_HEIGHT / simMinWidth

simWidth = SCREEN_WIDTH / cscale[0]
simHeight = SCREEN_HEIGHT / cscale[1]

def scale(x, y):
    return x * cscale[0], y * cscale[1]

#init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Billard Balls Collision")


#vector maths
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self,v):
        self.x = v.x
        self.y = v.y

    def add(self, v):
        self.x += v.x
        self.y += v.y

    def sub(self, v):
        self.x -= v
        self.y -= v

    def mult(self, n):
        self.x *= n
        self.y *= n



    def div(self, n):
        self.x /= n
        self.y /= n

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def dot(self, v):
        if v is None:
            print("Error: 'v' is None")
            return 0  # Return a default value or raise an exception
        return self.x * v.x + self.y * v.y

    
    def cross(self, v):
        return self.x * v.y - self.y * v.x

    def normalize(self):
        mag = self.mag()
        if mag != 0:
            return Vector2(self.x / mag, self.y / mag)
        else:
            return Vector2(0, 0)  # Return a zero vector if the magnitude is zero


    def limit(self, max_magnitude):
        if self.mag() > max_magnitude:
            self.normalize()
            self.mult(max_magnitude)

    @staticmethod
    def distance(v1, v2):
        dx = v1.x - v2.x
        dy = v1.y - v2.y
        return math.sqrt(dx * dx + dy * dy)
    
    def copy(self):
        return Vector2(self.x, self.y)

    @classmethod
    def clone(cls, v):
        return cls(v.x, v.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

class Ball:
    def __init__(self, x, y, radius, color, velocity=Vector2(0, 0), mass=1):
        self.pos = Vector2(x, y)
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.mass = mass

    def move(self):
        self.pos.add(self.velocity)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def check_boundary_collision(self, screen_width, screen_height):
        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > screen_width:
            self.velocity.x *= -1
        if self.pos.y - self.radius < 0 or self.pos.y + self.radius > screen_height:
            self.velocity.y *= -1
    
    def check_ball_collision(self, other_ball):
        # Calculate the vector between the centers of the two balls
        distance_vector = Vector2(other_ball.pos.x - self.pos.x, other_ball.pos.y - self.pos.y)

        # Calculate the distance between the centers of the two balls
        distance = distance_vector.mag()

        # Check if there is a collision
        if distance < self.radius + other_ball.radius:
            # Calculate the collision normal
            collision_normal = distance_vector.normalize()

            # Calculate the relative velocity
            relative_velocity = Vector2(other_ball.velocity.x - self.velocity.x, other_ball.velocity.y - self.velocity.y)

            # Calculate the relative velocity in the direction of the collision
            relative_speed = relative_velocity.dot(collision_normal)

            # Check if the balls are moving toward each other
            if relative_speed < 0:
                # Calculate the impulse scalar
                impulse_scalar = -(1 + 0.9) * relative_speed
                impulse_scalar /= 1 / self.mass + 1 / other_ball.mass

                # Apply impulses
                self.velocity.x -= impulse_scalar / self.mass * collision_normal.x
                self.velocity.y -= impulse_scalar / self.mass * collision_normal.y
                other_ball.velocity.x += impulse_scalar / other_ball.mass * collision_normal.x
                other_ball.velocity.y += impulse_scalar / other_ball.mass * collision_normal.y

                # Move the balls apart
                overlap = 0.5 * (distance - self.radius - other_ball.radius + 1)
                self.pos.x -= overlap * collision_normal.x
                self.pos.y -= overlap * collision_normal.y
                other_ball.pos.x += overlap * collision_normal.x
                other_ball.pos.y += overlap * collision_normal.y
# Create instances of Ball
balls = []
for i in range(4):
    balls.append(Ball(random.randint(0, SCREEN_WIDTH-6), random.randint(0, SCREEN_HEIGHT-6), 30, THECOLORS[random.choice(colours_list)], Vector2(random.randint(-5, 5), random.randint(-5, 5))))
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Move and draw the balls
    for ball in balls:
        ball.move()
        ball.draw(screen)


    # Check for boundary collisions
    for ball in balls:
        ball.check_boundary_collision(SCREEN_WIDTH, SCREEN_HEIGHT)


    # Check for ball-ball collisions
    for ball in balls:
        for other_ball in balls:
            if ball != other_ball:
                ball.check_ball_collision(other_ball)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
