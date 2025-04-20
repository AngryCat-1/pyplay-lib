from OpenGL.raw.GLUT import GLUT_LEFT_BUTTON

class BaseComponent:
    def __init__(self, name="Default Component", game_object=None, fields={}):
        self.name = name
        self.game_object = game_object
        self.fields = fields if fields else {}

    def start(self):
        pass

    def awake(self):
        pass

    def update(self, delta_time):
        pass

    def on_enable(self):
        pass

    def on_disable(self):
        pass

    def on_destroy(self):
        pass

    def get_component(self, cls):
        return self.game_object.get_component(cls) if self.game_object else None

    def get_field(self, name, default=None):
        return self.fields.get(name, default)

    def set_field(self, name, value):
        self.fields[name] = value

    def on_collision(self, other):
        pass

