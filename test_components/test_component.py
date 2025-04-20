import time

import keyboard_mover
from base_classes.component import BaseComponent
from base_classes.game_object import BaseGameObject
from base_classes.sprite import Sprite
from base_classes.vectors import Vector2
from engine import globals

class Mover(BaseComponent):
    def __init__(self, name="Mover", game_object=None, fields=None):
        super().__init__(name, game_object, fields)


    def update(self):
        self.game_object.rotate(1)


    def start(self):
        obj_child = BaseGameObject(
            name=f"2 Box",
            position=Vector2(300, 0),
            sprite=Sprite("engine/assets/square_red.png"),
            layer=1,
            rotation=22,
        )

        self.game_object.add_component(keyboard_mover.KeyboardMover())
        globals.scene.add_game_object(obj_child)

    def on_enable(self):
        pass

    def on_disable(self):
        pass
