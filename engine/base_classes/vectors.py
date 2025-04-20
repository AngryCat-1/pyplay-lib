import math


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2(x={self.x}, y={self.y})"

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand for *: Vector2 and " + str(type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other != 0:
                return Vector2(self.x / other, self.y / other)
            else:
                return Vector2(0, 0)
        return Vector2(self.x / other.x, self.y / other.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector2(0, 0)
        return self / l
