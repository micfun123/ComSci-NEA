#py games billard balls collision

import sys
import math
import random



#screen
screen_width = 800
screen_height = 600

simMinWidth = 2
cscale = screen_width / simMinWidth, screen_height / simMinWidth

simWidth = screen_width / cscale[0]
simHeight = screen_height / cscale[1]

def scale(x, y):
    return x * cscale[0], y * cscale[1]



#vector maths
class vector2:
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
    

