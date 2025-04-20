import collision_manager
from components import colider
#from components.rigidbody import RigidBody
from engine.base_classes.scene import BaseScene
from engine.base_classes.game_object import BaseGameObject
from engine.base_classes.camera import BaseCamera
from engine.base_classes.sprite import Sprite
from engine.base_classes.vectors import Vector2
from engine import core
from engine import globals
from test_components import keyboard_mover, test_component

scene = BaseScene("My Scene")
scene.clear_scene()
globals.scene = scene
camera = BaseCamera(position=Vector2(0,0), resolution=Vector2(800, 600))
scene.active_camera = camera


obj_player = BaseGameObject(
    name=f"Player Box",
    position=Vector2(350, 350),
    sprite=Sprite("engine/assets/player1.png"),
    scale=Vector2(1, 1),
    rotation=180,
    layer=12
)

obj_colider2 = BaseGameObject(
    name=f"Parent Box",
    position=Vector2(500, 200),
    sprite=Sprite("engine/assets/square_red.png"),
    scale=Vector2(1, 1),
    rotation=0,
    layer=11
)


obj_test = BaseGameObject(
    name=f"Test Box",
    position=Vector2(0, 0),
    sprite=Sprite("engine/assets/square.png"),
    scale=Vector2(100, 100),
    rotation=0,
    layer=10
)

obj_player.add_component(colider.PolygonCollider())
obj_colider2.add_component(colider.BoxCollider())
obj_player.add_component(keyboard_mover.KeyboardMover())

scene.add_game_object(obj_player)
scene.add_game_object(obj_colider2)
scene.add_game_object(obj_test)

core.start(scene)
