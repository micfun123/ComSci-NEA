#py games billard balls collision

import sys
import math
import random
import pygame
from pygame.locals import *
from pygame.color import THECOLORS



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
        self.x -= v.x
        self.y -= v.y

    def mult(self, n):
        self.x *= n
        self.y *= n

    def div(self, n):
        self.x /= n
        self.y /= n

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def dot(self, v):
        return self.x * v.x + self.y * v.y
    
    def cross(self, v):
        return self.x * v.y - self.y * v.x

    def normalize(self):
        mag = self.mag()
        if mag != 0:
            self.div(mag)

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
    def __init__(self, x, y, radius, color, velocity=Vector2(0, 0)):
        self.pos = Vector2(x, y)
        self.radius = radius
        self.color = color
        self.velocity = velocity

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
        distance = Vector2.distance(self.pos, other_ball.pos)
        if distance < self.radius + other_ball.radius:
            # Calculate the collision normal (unit vector pointing from self to other_ball)
            collision_normal = Vector2.normalize(Vector2(other_ball.pos.x - self.pos.x, other_ball.pos.y - self.pos.y))

            # Calculate the relative velocity
            relative_velocity = Vector2(other_ball.velocity.x - self.velocity.x, other_ball.velocity.y - self.velocity.y)

            # Calculate the dot product of relative velocity and collision normal
            dot_product = relative_velocity.dot(collision_normal)

            # Calculate impulse (change in velocity)
            impulse = (2.0 * dot_product) / (1.0 + 1.0)  # Assuming equal mass (1.0) for both balls

            # Update velocities
            self.velocity.add(Vector2(impulse * collision_normal.x, impulse * collision_normal.y))
            other_ball.velocity.sub(Vector2(impulse * collision_normal.x, impulse * collision_normal.y))

# Create instances of Ball
ball1 = Ball(200, 200, 20, (0, 0, 255), Vector2(5, 2))
ball2 = Ball(400, 400, 30, (255, 0, 0), Vector2(-3, -1))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Move and draw the balls
    ball1.move()
    ball2.move()
    ball1.draw(screen)
    ball2.draw(screen)

    # Check for boundary collisions
    ball1.check_boundary_collision(SCREEN_WIDTH, SCREEN_HEIGHT)
    ball2.check_boundary_collision(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Check for ball-ball collisions
    ball1.check_ball_collision(ball2)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
