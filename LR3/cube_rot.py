from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np
from sys import exit
from pyglet import clock

# Проецирование
rot_x = 15  # Углы поворота вокруг осей X, Y и Z
rot_y = 25  # (15, 25, 15) или (-25, 215, -15)
rot_z = 15
# Вращение
n_rot, da = 0, 5
#
R = 30  # Радиус окружности (для построения треугольника)
h = R // 5  # Половина длины ребра куба
w = R + 2 * h  # Для задания области вывода
width = height = 400  # Размер окна вывода
# Координаты вершин треугольника
ang = np.pi / 6
v0 = (-R * np.cos(ang), -R * np.sin(ang), 0)
v1 = (-v0[0], v0[1], 0)
v2 = (0, R, 0)
# Кубик
verts = ((h, -h, -h),  # Координаты вершин куба
         (h, h, -h),
         (-h, h, -h),
         (-h, -h, -h),
         (h, -h, h),
         (h, h, h),
         (-h, -h, h),
         (-h, h, h))
faces = ((0, 1, 2, 3),  # Индексы вершин граней куба
         (3, 2, 7, 6),
         (6, 7, 5, 4),
         (4, 5, 1, 0),
         (1, 5, 7, 2),
         (4, 0, 3, 6))
clrs = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
        (0, 1, 1), (1, 1, 1), (1, 0, 0), (0, 1, 0),
        (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 1, 1))


def t_draw():
    graphics.draw(3, GL_LINE_LOOP, ('v3f', v0 + v1 + v2), ('c3f', [1, 0, 0] * 3))


def cube_draw():
    k = -1
    for face in faces:
        k += 1
        m = -1
        v4, c4 = (), ()
        for v in face:
            m += 1
            v4 += verts[v]
            c4 += clrs[k + m]
        graphics.draw(4, GL_QUADS, ('v3f', v4), ('c3f', c4))


window = Window(visible=True, width=width, height=height, resizable=True)
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glLineWidth(6)


def rot(dt):
    global n_rot, da
    if abs(n_rot) > 180:
        da = -da
    n_rot += da


clock.schedule_interval(rot, 0.15)


@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)  # Проецирование
    glLoadIdentity()
    glOrtho(-w, w, -w, w, -w, w)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    t_draw()
    glPushMatrix()
    glRotatef(n_rot, 1, 0, 0)
    glRotatef(n_rot, 0, 1, 0)
    glRotatef(n_rot, 0, 0, 1)
    cube_draw()
    glPopMatrix()


@window.event
def on_key_press(char, modifiers):
    global n_rot, da
    if char == key._1:
        if abs(n_rot) > 180:
            da = -da
        n_rot += da


app.run()
