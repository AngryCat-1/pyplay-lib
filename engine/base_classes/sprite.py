import os
from PIL import Image


class Sprite:
    def __init__(self, image_path=""):
        self.image_path = image_path

    def __repr__(self):
        return f"<Sprite path='{self.image_path}'>"

    def get_size(self):
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Image not found: {self.image_path}")
        with Image.open(self.image_path) as img:
            return img.size
