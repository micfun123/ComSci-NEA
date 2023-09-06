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
        return vector2(self.x, self.y)

    @classmethod
    def clone(cls, v):
        return cls(v.x, v.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

#test vector2
def test_vector2():
    items = []
    items.append(vector2(1, 2))
    items.append(vector2(3, 4))
    items.append(vector2(5, 6))
    for i in items:
        print(i)
    print("distance: {}".format(vector2.distance(items[0], items[1])))
    print("dot: {}".format(items[0].dot(items[1])))
    print("cross: {}".format(items[0].cross(items[1])))
    

print("vector2 test")
test_vector2()
