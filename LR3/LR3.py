# Разместить кубик в каждой вершине правильного треугольника (центр кубика находится в вершине).
# Обеспечить вращение кубиков вокруг своих центров, а также вращение треугольника вместе с кубиками
# вокруг оси Z. Использовать изометрическое проецирование и clock.schedule_interval.

from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window, key
from pyglet import clock
import numpy as np

# Проецирование
rot_x = 15
rot_y = 25
rot_z = 15
# Вращение
n_rot, da = 0, 5
c1_rot, c1a = 0, 9
c2_rot, c2a = 0, 6
c3_rot, c3a = 0, 3
#
R = 30  # Радиус окружности (для построения треугольника)
h = R // 4  # Половина длины ребра куба
w = R + 2 * h  # Для задания области вывода
width = height = 400  # Размер окна вывода

textureIDs = (gl.GLuint * 6)()  # Массив идентификаторов (номеров) текстур
p = GL_TEXTURE_2D
tc = 1  # Число повторов текстуры

# Координаты вершин треугольника
ang = np.pi / 6
v0 = (-R * np.cos(ang), -R * np.sin(ang), 0)
v1 = (-v0[0], v0[1], 0)
v2 = (0, R, 0)
# Кубик
vert = ((h, -h, -h),  # шаблон для координат вершин у куба
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
t_cs = ((0, 0), (0, tc), (tc, tc), (tc, 0))


def texInit():  # Формирование текстур
    glGenTextures(6, textureIDs)
    r = GL_RGB
    p3 = GL_REPEAT # GL_REPEAT GL_CLAMP_TO_EDGE
    p4 = GL_LINEAR
    for k in range(6):
        iWidth = iHeight = 64  # Размер текстуры равен iWidth * iHeight
        n = 3 * iWidth * iHeight
        img = np.zeros((3, iWidth, iHeight), dtype='uint8')
        for i in range(iHeight):  # Генерация черно-белого образа, на основе которого создается текстура
            for j in range(iWidth):
                img[:, i, j] = ((i - 1) & 16 ^ (j - 1) & 16) * 255
        img = img.reshape(n)
        img = (GLubyte * n)(*img)
        glBindTexture(p, textureIDs[k])
        glTexParameterf(p, GL_TEXTURE_WRAP_S, p3)
        glTexParameterf(p, GL_TEXTURE_WRAP_T, p3)
        glTexParameterf(p, GL_TEXTURE_MAG_FILTER, p4)
        glTexParameterf(p, GL_TEXTURE_MIN_FILTER, p4)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, GL_UNSIGNED_BYTE, img)
    glEnable(p)


def t_draw():
    graphics.draw(3, GL_LINE_LOOP, ('v3f', v0 + v1 + v2), ('c3f', [0, 1, 0] * 3))


def cube_draw():
    k = -1
    for face in faces:
        k += 1
        m = -1
        v4, c4, t4 = (), (), ()
        gl.glBindTexture(p, textureIDs[k])
        for v in face:
            m += 1
            v4 += vert[v]
            c4 += clrs[k + m]
            t4 += t_cs[m]
        graphics.draw(4, GL_QUADS, ('v3f', v4), ('c3f', c4), ('t2f', t4))


def triag_rot(dt):
    global n_rot, da
    if abs(n_rot) > 270:
        da = -da
    n_rot += da


def cube1_rot(dt):
    global c1_rot, c1a
    if abs(c1_rot) > 360:
        c1a = -c1a
    c1_rot += c1a


def cube2_rot(dt):
    global c2_rot, c2a
    if abs(c2_rot) > 360:
        c2a = -c2a
    c2_rot += c2a


def cube3_rot(dt):
    global c3_rot, c3a
    if abs(c3_rot) > 360:
        c3a = -c3a
    c3_rot += c3a


clock.schedule_interval(triag_rot, 0.15)
clock.schedule_interval(cube1_rot, 0.30)
clock.schedule_interval(cube2_rot, 0.40)
clock.schedule_interval(cube3_rot, 0.55)


window = Window(visible=True, width=width, height=height, resizable=True, caption="triag_cubes")
glClearColor(0.4, 0.4, 0.4, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glLineWidth(6)
texInit()


@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)  # Проецирование
    glLoadIdentity()
    glOrtho(-w, w, -w, w, -w, w)
    glRotatef(rot_x + n_rot, 1, 0, 0)
    glRotatef(rot_y + n_rot, 0, 1, 0)
    glRotatef(rot_z + n_rot, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    t_draw()
    glPopMatrix()
    glLoadIdentity()
    glTranslatef(v0[0], v0[1], v0[2])
    glRotatef(c1_rot, 1, 1, 1)
    cube_draw()
    glLoadIdentity()
    glTranslatef(v1[0], v1[1], v1[2])
    glRotatef(c2_rot, 1, 1, 1)
    cube_draw()
    glLoadIdentity()
    glTranslatef(v2[0], v2[1], v2[2])
    glRotatef(c3_rot, 1, 1, 1)
    cube_draw()


app.run()
