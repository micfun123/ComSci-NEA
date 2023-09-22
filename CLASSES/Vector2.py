import math

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
