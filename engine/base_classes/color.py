class ColorRGB:
    def __init__(self, r=255, g=255, b=255):
        self.r = self._clamp(r)
        self.g = self._clamp(g)
        self.b = self._clamp(b)

    def _clamp(self, value):
        return max(0, min(255, int(value)))

    def to_tuple(self):
        return (self.r, self.g, self.b)

    def __repr__(self):
        return f"ColorRGB(r={self.r}, g={self.g}, b={self.b})"


class ColorRGBA(ColorRGB):
    def __init__(self, r=255, g=255, b=255, a=255):
        super().__init__(r, g, b)
        self.a = self._clamp(a)

    def to_tuple(self):
        return (self.r, self.g, self.b, self.a)

    def __repr__(self):
        return f"ColorRGBA(r={self.r}, g={self.g}, b={self.b}, a={self.a})"
