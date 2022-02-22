import pyglet
from pyglet.app import *
from pyglet.gl import *
from pyglet.graphics import *
from pyglet.window import Window, key
import numpy as np

w = 400
# vp = np.full((w, w, 3), 255, dtype='uint8')   # для фона
d = 15
wx, wy = 1.2 * d, 1.2 * d   # Параметры области визуализации
# width, height = w, w        # Размеры окна вывода
# vp[:, -30:] = [0, 0, 255]   # правая
# vp[:, :30] = [0, 0, 255]    # левая
# vp = vp.flatten()
# vp = (GLubyte * (w * w * 3))(*vp)

window = Window(visible=True, width=int(20 * wx), height=int(20 * wy),
                resizable=True, caption='НЕ флаг Израиля')

glClearColor(0.8, 0.8, 0.8, 1.0)
glClear(GL_COLOR_BUFFER_BIT)

glEnable(gl.GL_POINT_SMOOTH)
glPointSize(10)
glLineWidth(4)

glPolygonMode(GL_FRONT, GL_POINT)  # лицевая сторона - вершины
glPolygonMode(GL_BACK, GL_LINE)  # нелицевая сторона - линии

mode_fs = GL_POINT
mode_bs = GL_LINE
shade_model = GL_SMOOTH
px = py = 0
flag = False  # шаблон для линий вкл/выкл


@window.event
def on_draw():
    window.clear()
    # glDrawPixels(w, w, GL_RGB, GL_UNSIGNED_BYTE, vp)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glRotatef(180 * px, 1, 0, 0)  # Поворот вокруг оси X
    glRotatef(180 * py, 0, 1, 0)  # Поворот вокруг оси Y
    glOrtho(-wx, wx, -wy, wy, -1, 1)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    glVertex3f(0, -d, 0)
    glColor3f(0, 0, 1)
    glVertex3f(d/2, d * 2/3, 0)
    glColor3f(1, 0, 0)
    glVertex3f(-d/2, d * 2/3, 0)
    glColor3f(0, 0.5, 0)
    glVertex3f(0, d, 0)
    glColor3f(0, 0, 0.5)
    glVertex3f(-d / 2, -d * 2 / 3, 0)
    glColor3f(0.5, 0, 0)
    glVertex3f(d/2, -d * 2/3, 0)
    glEnd()


@window.event
def on_key_press(symbol, modifiers):
    global mode_fs, mode_bs, shade_model, px, py, flag
    if symbol == key._1:  # поворот относительно OX
        px = 1 - px
        py = 0
    elif symbol == key._2:  # поворот относительно OY
        px = 0
        py = 1 - py
    elif symbol == key._3:  # изменения режима интерполяции
        if shade_model == GL_SMOOTH:
            shade_model = GL_FLAT
        else:
            shade_model = GL_SMOOTH
    elif symbol == key._4:  # отключение/включение шаблона для линий
        if mode_fs == GL_LINE or mode_bs == GL_LINE:
            if not flag:
                gl.glEnable(gl.GL_LINE_STIPPLE)
                pattern = '0b1111100110011111'
                gl.glLineStipple(2, int(pattern, 2))
                flag = True
            else:
                gl.glDisable(gl.GL_LINE_STIPPLE)
                flag = False
    elif symbol == key._5:  # лицевая сторона - точки
        mode_fs = GL_POINT
    elif symbol == key._6:  # нелицевая сторона - точки
        mode_bs = GL_POINT
    elif symbol == key._7:  # лицевая сторона - линии
        mode_fs = GL_LINE
    elif symbol == key._8:  # нелицевая сторона - линии
        mode_bs = GL_LINE
    elif symbol == key._9:  # лицевая сторона - заливка
        mode_fs = GL_FILL
    elif symbol == key._0:  # нелицевая сторона - заливка
        mode_bs = GL_FILL

    glPolygonMode(GL_FRONT, mode_fs)  # лицевая сторона
    glPolygonMode(GL_BACK, mode_bs)  # нелицевая сторона
    gl.glShadeModel(shade_model)


run()
