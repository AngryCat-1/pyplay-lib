import os
import time

import numpy as np
from OpenGL.GL import *
from PIL import Image
from math import cos, sin, radians
from skimage import measure

import collision_manager
from base_classes.component import BaseComponent
from engine import globals


class ColliderComponent(BaseComponent):
    def __init__(self, name="BaseCollider", game_object=None, fields={}):
        super().__init__(name, game_object, fields)
        self.is_trigger = fields.get("is_trigger", False)
        self.colliding = False
        self._last_blink_time = time.time()
        self._blink_state = True

    def awake(self):
        collision_manager.cls_manager.register(self)

    def transform_point(self, x, y):
        pos = self.game_object.get_world_position()
        scale = self.game_object.scale
        rotation = radians(self.game_object.rotation)
        x *= scale.x
        y *= scale.y
        rotated_x = cos(rotation) * x - sin(rotation) * y
        rotated_y = sin(rotation) * x + cos(rotation) * y
        return pos.x + rotated_x, pos.y + rotated_y

    def draw(self):
        if globals.SHOW_COLLIDERS:
            self._draw_bounds()

    def _draw_bounds(self):
        pass

    def _draw_circle(self, x, y, radius, segments=12):
        if self.colliding:
            blink = abs(np.sin(time.time() * 10))
            glColor4f(blink, 0, 0, 1)
        else:
            glColor4f(0, 0, 1, 1)


        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            dx = radius * np.cos(angle)
            dy = radius * np.sin(angle)
            glVertex2f(x + dx, y + dy)
        glEnd()

        glColor4f(1, 1, 1, 1)


class BoxCollider(ColliderComponent):
    def __init__(self, name="BoxCollider", game_object=None, fields={}):
        super().__init__(name, game_object, fields)

    def get_bounds(self):
        pos = self.game_object.get_world_position()
        sprite = self.game_object.sprite
        if sprite:
            width, height = sprite.get_size()
        else:
            width = height = 50
        scale = self.game_object.scale
        width *= scale.x
        height *= scale.y
        return (
            pos.x - width / 2,
            pos.y - height / 2,
            pos.x + width / 2,
            pos.y + height / 2
        )

    def _draw_bounds(self):
        sprite = self.game_object.sprite
        if sprite:
            width, height = sprite.get_size()
        else:
            width = height = 50
        scale = self.game_object.scale
        width *= scale.x
        height *= scale.y
        hw, hh = width / 2, height / 2
        corners = [
            (-hw, -hh),
            (hw, -hh),
            (hw, hh),
            (-hw, hh)
        ]
        for x, y in corners:
            wx, wy = self.transform_point(x, y)
            self._draw_circle(wx, wy, 6)


class PolygonCollider(ColliderComponent):
    def __init__(self, name="PolygonCollider", game_object=None, fields={}):
        super().__init__(name, game_object, fields)
        self.local_points = []

    def awake(self):
        super().awake()
        sprite = self.game_object.sprite
        if not sprite:
            return

        path = sprite.image_path
        if not os.path.exists(path):
            return

        img = Image.open(path).convert("RGBA")
        alpha = img.split()[-1]
        alpha_data = np.array(alpha)

        binary = alpha_data > 10

        padded = np.pad(binary, pad_width=1, mode='constant', constant_values=False)

        contours = measure.find_contours(padded.astype(float), 0.5)
        if not contours:
            print("PolygonCollider: no contours found")
            return

        largest = max(contours, key=len)
        img_width, img_height = img.size

        self.local_points = []
        for y, x in largest:
            cx = (x - 1) - img_width / 2
            cy = img_height / 2 - (y - 1)
            self.local_points.append((cx, cy))


    def get_bounds(self):
        if not self.local_points:
            return (0, 0, 0, 0)

        world_points = [self.transform_point(x, y) for x, y in self.local_points]
        xs = [p[0] for p in world_points]
        ys = [p[1] for p in world_points]
        return (min(xs), min(ys), max(xs), max(ys))

    def _draw_bounds(self):
        for x, y in self.local_points:
            wx, wy = self.transform_point(x, y)
            self._draw_circle(wx, wy, 2)

