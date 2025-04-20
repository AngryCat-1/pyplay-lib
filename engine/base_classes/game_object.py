import math
from engine.base_classes.color import ColorRGB, ColorRGBA
from engine.base_classes.vectors import Vector2

class BaseGameObject:
    def __init__(
        self,
        name="Default Game Object",
        position=Vector2(0, 0),
        rotation=0,
        scale=Vector2(1, 1),
        sprite=None,
        components=None,
        active=True,
        parent=None,
        layer=0,
        children=[]
    ):
        self.name = name
        self.position = position
        self.rotation = rotation
        self.scale = scale

        self.sprite = sprite
        self.components = components or []

        self.active = active
        self.parent = parent
        self.layer = layer
        self.children = children
        self.started = False

    def get_world_position(self):
        if self.parent:
            parent_pos = self.parent.get_world_position()
            parent_rot = self.parent.get_world_rotation()
            parent_scale = self.parent.get_world_scale()

            local = self.position * parent_scale
            angle_rad = math.radians(parent_rot)

            rotated_x = local.x * math.cos(angle_rad) - local.y * math.sin(angle_rad)
            rotated_y = local.x * math.sin(angle_rad) + local.y * math.cos(angle_rad)

            return parent_pos + Vector2(rotated_x, rotated_y)
        return self.position

    def get_world_rotation(self):
        if self.parent:
            return self.parent.get_world_rotation() + self.rotation
        return self.rotation

    def get_world_scale(self):
        if self.parent:
            parent_scale = self.parent.get_world_scale()
            return Vector2(self.scale.x * parent_scale.x, self.scale.y * parent_scale.y)
        return self.scale

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parent = self

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def add_component(self, component):
        component.game_object = self
        self.components.append(component)
        component.awake()
        component.start()

    def get_component(self, component_type):
        return next((comp for comp in self.components if isinstance(comp, component_type)), None)

    def get_components(self, component_type):
        return [comp for comp in self.components if isinstance(comp, component_type)]

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)

    def move(self, dx, dy):
        self.position.x += dx
        self.position.y += dy

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def rotate(self, angle):
        self.rotation += angle

    def set_rotation(self, angle):
        self.rotation = angle

    def set_scale(self, x, y):
        self.scale.x = x
        self.scale.y = y

    def activate(self):
        self.active = True
        for comp in self.components:
            comp.on_enable()

    def deactivate(self):
        self.active = False
        for comp in self.components:
            comp.on_disable()

    def destroy(self):
        for comp in self.components:
            comp.on_destroy()
        del self

    def set_layer(self, layer):
        self.layer = layer

    def set_sprite(self, sprite_path):
        self.sprite = sprite_path

    def attach_to(self, parent_object):
        self.parent = parent_object

    def detach(self):
        self.parent = None

    def update(self, delta_time):
        if self.active:
            for comp in self.components:
                comp.update(delta_time)

    def __repr__(self):
        return f"<GameObject '{self.name}' pos={self.position} sprite={'Yes' if self.sprite else 'No'}>"
