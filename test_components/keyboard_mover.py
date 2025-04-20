from pynput import keyboard
from threading import Thread
from base_classes.component import BaseComponent
from base_classes.vectors import Vector2
import time


class KeyboardMover(BaseComponent):
    def __init__(self, name="KeyboardMover", game_object=None, fields=None):
        super().__init__(name, game_object, fields)
        self._keys = set()
        self._running = True
        self._speed = 100
        self._listener = None
        self._listener_thread = Thread(target=self._keyboard_listener, daemon=True)
        self._movement_thread = Thread(target=self._movement_loop, daemon=True)

    def start(self):
        self._listener_thread.start()
        self._movement_thread.start()

    def _keyboard_listener(self):
        def on_press(key):
            try:
                self._keys.add(key.char.lower())
            except AttributeError:
                pass

        def on_release(key):
            try:
                self._keys.discard(key.char.lower())
            except AttributeError:
                pass

        self._listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._listener.start()
        self._listener.join()

    def _movement_loop(self):
        prev_time = time.time()
        while self._running:
            time.sleep(0.01)
            now = time.time()
            dt = now - prev_time
            prev_time = now

            if not self.game_object:
                continue

            direction = Vector2(0, 0)
            if "w" in self._keys:
                direction.y -= 1
            if "s" in self._keys:
                direction.y += 1
            if "a" in self._keys:
                direction.x -= 1
            if "d" in self._keys:
                direction.x += 1

            if direction.x != 0 or direction.y != 0:
                movement = direction.normalized() * self._speed * dt
                self.game_object.position += movement

    def on_disable(self):
        self._running = False
        if self._listener:
            self._listener.stop()

    def on_collision(self, other_collider):
        pass
