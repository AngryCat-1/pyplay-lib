from engine.base_classes.game_object import BaseGameObject
from engine.base_classes.color import ColorRGB
from engine.base_classes.vectors import Vector2

class Light2D(BaseGameObject):
    def __init__(
        self,
        name="Light",
        position=Vector2(0, 0),
        color=ColorRGB(255, 255, 255),
        intensity=1.0
    ):
        super().__init__(name=name, position=position)
        self.color = color
        self.intensity = intensity

    def __repr__(self):
        return f"<Light2D {self.name} at {self.position} intensity={self.intensity}>"
