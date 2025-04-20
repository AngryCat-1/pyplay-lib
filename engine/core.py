import asyncio
import time

import collision_manager
from engine.base_classes.scene import BaseScene
from engine.base_classes.game_object import BaseGameObject
from engine.base_classes.camera import BaseCamera
from engine.base_classes.sprite import Sprite
from engine.base_classes.vectors import Vector2
from engine import renderer

FPS = 60
SHOW_COLLIDERS = True


def start(scene):
    renderer.start_rendering(scene)
    while True:
        renderer.render_scene()
        update_function(scene)
        time.sleep(1/FPS)


def update_function(scene):
    for obj in scene.game_objects:
        if obj.active:
           obj.update()
