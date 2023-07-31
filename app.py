#py games billard balls collision

import pygame
import sys
import random

pygame.init()

#screen
screen_width = 800
screen_height = 600

simMinWidth = 2
cscale = screen_width / simMinWidth, screen_height / simMinWidth

print(cscale)
simWidth = screen_width / cscale[0]
simHeight = screen_height / cscale[1]

def scale(x, y):
    return x * cscale[0], y * cscale[1]

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Billard Balls")

#vector maths
class vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self,v):
        self.x = v.x
        self.y = v.y