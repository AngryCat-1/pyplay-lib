import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
import os
import math
import collision_manager
import globals
from components.colider import ColliderComponent
from engine.exceptor import get_except

_scene = None
_loaded_textures = {}
_FPS = 60
_MS_PER_FRAME = int(1000 / _FPS)


def init_opengl(width, height):
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_TEXTURE_2D)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)


def load_texture(image_path):
    if image_path in _loaded_textures:
        return _loaded_textures[image_path]

    if not os.path.exists(image_path):
        get_except(f"Image not found: {image_path}")
        return None

    img = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    _loaded_textures[image_path] = (texture_id, img.width, img.height)
    return _loaded_textures[image_path]


def draw_sprite(x, y, sprite, camera_offset, rotation, scale):
    texture_info = load_texture(sprite.image_path)
    if not texture_info:
        return

    texture_id, width, height = texture_info
    # print(f'Coordinate: {x}, {y}')
    # print(f'Width: {width}, Height: {height}')
    # print(f'Camera offset: {camera_offset[0]}, {camera_offset[1]}')

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glPushMatrix()
    glTranslatef(x - camera_offset[0], y - camera_offset[1], 0)
    glRotatef(rotation, 0, 0, 1)
    glScalef(scale.x, scale.y, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-width / 2, -height / 2)
    glTexCoord2f(1, 0); glVertex2f(width / 2, -height / 2)
    glTexCoord2f(1, 1); glVertex2f(width / 2, height / 2)
    glTexCoord2f(0, 1); glVertex2f(-width / 2, height / 2)


    # print(f'RENDER: x1 - {x - width / 2}, y1 - {y - height / 2 }, x2 - {x + width / 2}, y2 - {y + height / 2}')

    glEnd()

    glPopMatrix()


def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    camera = _scene.active_camera
    if camera:
        cam_x = camera.position.x
        cam_y = camera.position.y
    else:
        cam_x, cam_y = 0, 0

    sorted_objects = sorted(_scene.game_objects, key=lambda o: o.layer)

    for obj in sorted_objects:
        if not obj.active or not obj.sprite:
            continue

        world_pos = obj.get_world_position()
        world_rot = obj.get_world_rotation()
        world_scale = obj.get_world_scale()

        draw_sprite(world_pos.x, world_pos.y, obj.sprite, (cam_x, cam_y), world_rot, world_scale)

        for component in obj.get_components(ColliderComponent):
            component.draw()

    glutSwapBuffers()

_last_time = time.time()


def update(_=None):
    global _last_time

    now = time.time()
    delta_time = now - _last_time
    _last_time = now

    for obj in _scene.game_objects:
        if obj.active:
            obj.update(delta_time)

    collision_manager.cls_manager.check_collisions()

    glutPostRedisplay()
    glutTimerFunc(_MS_PER_FRAME, update, 0)

def start_rendering(scene, fps=60):
    global _scene, _FPS, _MS_PER_FRAME
    _scene = scene
    _FPS = fps
    _MS_PER_FRAME = int(1000 / fps)

    cam = scene.active_camera
    if cam:
        width, height = int(cam.resolution.x), int(cam.resolution.y)
    else:
        width, height = 800, 600

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Game")

    init_opengl(width, height)

    glutDisplayFunc(render_scene)
    glutTimerFunc(_MS_PER_FRAME, update, 0)  # запустить обновление
    glutMainLoop()
