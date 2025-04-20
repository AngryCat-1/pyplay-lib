from engine.base_classes.vectors import Vector2
from engine.base_classes.game_object import BaseGameObject

class BaseCamera(BaseGameObject):
    def __init__(
        self,
        name="Camera",
        position=Vector2(0, 0),
        resolution=Vector2(800, 600),
        is_active_camera=True
    ):
        super().__init__(name=name, position=position)
        self.resolution = resolution
        self.is_active_camera = is_active_camera

    def __repr__(self):
        return f"<Camera {self.name} res={self.resolution} pos={self.position}>"
