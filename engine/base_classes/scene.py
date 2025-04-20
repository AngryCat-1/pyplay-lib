class BaseScene:
    def __init__(self, name="Default Scene Name", game_objects=None, active_camera=None):
        self.name = name
        self.game_objects = game_objects if game_objects is not None else []
        self.active_camera = active_camera

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object):
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)

    def get_game_object_by_name(self, name):
        return next((obj for obj in self.game_objects if obj.name == name), None)

    def get_all_active_objects(self):
        return [obj for obj in self.game_objects if obj.active]

    def clear_scene(self):
        self.game_objects.clear()

    def set_active_camera(self, camera):
        self.active_camera = camera

    def get_objects_in_layer(self, layer):
        return [obj for obj in self.game_objects if obj.layer == layer]

    def sort_objects_by_layer(self):
        self.game_objects.sort(key=lambda obj: obj.layer)

    def update_scene(self):
        for obj in self.game_objects:
            obj.update()

    def start_scene(self):
        for obj in self.game_objects:
            obj.start()




    def __repr__(self):
        return (
            f"BaseScene(name={self.name}, "
            f"game_objects={[obj.name for obj in self.game_objects]}, "
            f"active_camera={self.active_camera.name if self.active_camera else None})"
        )
