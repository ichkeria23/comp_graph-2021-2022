from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window
from pyglet import clock
import numpy as np

d, d1, d2 = 5, 10, 15
wx, wy = 1.5 * d2, 1.5 * d2
width, height = int(20 * wx), int(20 * wy)
tile_x, tile_y, d_tile = 1, 1, -0.5
n_rot, da = 1, 1
R, G, B = 1, 0, 0
d_rgb = 0.01


def to_c_float_Array(data):  # Преобразование в си-массив
    return (GLfloat * len(data))(*data)


vld = to_c_float_Array([-10, -10, 0])  # Левая нижняя вершина
vrd = to_c_float_Array([-10, 10, 0])  # Правая нижняя вершина
vru = to_c_float_Array([0, 10, 0])  # Правая верхняя вершина
vlu = to_c_float_Array([0, -10, 0])  # Левая верхняя вершина
vrn = to_c_float_Array([0, 10, 10])
vrt = to_c_float_Array([0, -10, 10])


glPolygonMode(GL_BACK, GL_FILL)
glPolygonMode(GL_FRONT, GL_FILL)


def isom():
    sinf = np.sqrt(1 / 3)
    cosf = np.sqrt(2 / 3)
    sinp = np.sqrt(1 / 2)
    cosp = np.sqrt(1 / 2)
    iso = np.array([[cosp,  sinf * sinp,  0, 0],
                   [0,            cosf,  0, 0],
                   [sinp, -sinf * cosp,  0, 0],
                   [0,               0,  0, 1]])
    iso = iso.flatten()
    iso = (GLfloat * 16)(*iso)
    return iso


def texInit():
    fn = 'C:\\Users\\user\\PycharmProjects\\third_task_kg\\cat.jpg'
    img = pyglet.image.load(fn)
    iWidth = img.width
    iHeight = img.height
    img = img.get_data('RGB', iWidth * 3)
    p = GL_TEXTURE_2D
    r = GL_RGB
    # Задаем параметры текстуры
    glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT)  # GL_CLAMP
    glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Способ взаимодействия с текущим фрагментом изображения
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    # Создаем 2d-текстуру на основе образа img
    glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, GL_UNSIGNED_BYTE, img)
    glEnable(p)


window = Window(visible=True, width=width, height=height,
                resizable=True, caption='LR4')
glClearColor(0.82, 0.69, 0.52, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

texInit()


@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    iso = isom()  # Изометрическое проецирование
    glLoadMatrixf(iso)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glOrtho(-wx, wx, -wy, wy, -wx, wx)
    glRotatef(n_rot, 0, 1, 0)
    # glColor3f(R, G, B)
    pyglet.graphics.draw(4, GL_QUADS,
                         ('v3f', (0, -10, 0, 0, 10, 0, 0, 10, 10, 0, -10, 10)),
                         ('c3f', (R, G, B) * 4),
                         ('t2f', (0, 0, 0, tile_y, tile_x, tile_y, tile_x, 0)))
    pyglet.graphics.draw(4, GL_QUADS,
                         ('v3f', (0, -10, 0,  0, 10, 0, 10, 10, 0, 10, -10, 0)),
                         # ('v3f', (0, 10, 0, 10, 10, 0, 10, -10, 0, 0, -10, 0)),
                         ('c3f', (R, G, B) * 4),
                         ('t2f', (0, 0, 0, tile_y, tile_x, tile_y, tile_x, 0)))


def tile(dt):
    global tile_x, tile_y, d_tile
    if tile_x == 1:
        d_tile = -d_tile
    if tile_x == 5:
        d_tile = -d_tile
    tile_x += d_tile
    tile_y += d_tile


def rotate(dt):
    global n_rot, da
    if n_rot == 360:
        da = -da
    if n_rot == 0:
        da = -da
    n_rot += da


def rgb(dt):
    global G, d_rgb
    if G == 1:
        d_rgb = -d_rgb
    if G == -0.01:
        d_rgb = -d_rgb
    G += d_rgb


clock.schedule_interval(tile, 0.3)
clock.schedule_interval(rotate, 0.01)
clock.schedule_interval(rgb, 0.01)


app.run()