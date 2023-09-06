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
        if v is None:
            print("Error: 'v' is None")
            return 0  # Return a default value or raise an exception
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
        # Calculate the relative velocity as the difference between the velocities of the two balls
        relative_velocity = Vector2(other_ball.velocity.x - self.velocity.x, other_ball.velocity.y - self.velocity.y)
    
        # Calculate the relative position as the difference between the positions of the two balls
        relative_position = Vector2(other_ball.pos.x - self.pos.x, other_ball.pos.y - self.pos.y)
    
        # Calculate the dot product of relative_position and relative_velocity
        dot_product = relative_position.dot(relative_velocity)
    
        # Check if the dot product is positive (balls are moving towards each other)
        if dot_product > 0:
            # Calculate the squared distance between the balls
            squared_distance = relative_position.x ** 2 + relative_position.y ** 2
    
            # Calculate the sum of the squared radii
            sum_of_radii_squared = (self.radius + other_ball.radius) ** 2
    
            # Check if the squared distance is less than the squared sum of radii (collision)
            if squared_distance < sum_of_radii_squared:
                # Calculate the distance between the balls
                distance = math.sqrt(squared_distance)
    
                # Calculate the penetration depth
                penetration_depth = self.radius + other_ball.radius - distance
    
                # Calculate the collision normal
                collision_normal = relative_position.normalize()
    
                # Calculate the impulse
                impulse = (2.0 * relative_velocity.dot(collision_normal)) / (1.0 + 1.0)
    
                # Calculate the change in position to resolve the penetration
                penetration_resolution = collision_normal.mult(penetration_depth / 2.0)
    
                # Update positions to resolve penetration
                self.pos.sub(penetration_resolution)
                other_ball.pos.add(penetration_resolution)
    
                # Update velocities
                self.velocity.add(collision_normal.mult(impulse))
                other_ball.velocity.sub(collision_normal.mult(impulse))
    


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
