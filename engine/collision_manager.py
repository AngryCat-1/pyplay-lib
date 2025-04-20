class CollisionManager:
    def __init__(self):
        self.colliders = []

    def clear(self):
        self.colliders = []

    def register(self, collider):
        self.colliders.append(collider)

    def unregister(self, collider):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def check_collisions(self):
        for collider in self.colliders:
            collider.colliding = False

        for i in range(len(self.colliders)):
            a = self.colliders[i]
            bounds_a = a.get_bounds()

            for j in range(i + 1, len(self.colliders)):
                b = self.colliders[j]
                bounds_b = b.get_bounds()

                if self._intersects(bounds_a, bounds_b):
                    a.colliding = True
                    b.colliding = True


                    for comp in a.game_object.components:
                        if hasattr(comp, "on_collision") and callable(comp.on_collision):
                            comp.on_collision(b)


                    for comp in b.game_object.components:
                        if hasattr(comp, "on_collision") and callable(comp.on_collision):
                            comp.on_collision(a)

    def _intersects(self, a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return not (ax2 <= bx1 or ax1 >= bx2 or ay2 <= by1 or ay1 >= by2)


cls_manager = CollisionManager()
