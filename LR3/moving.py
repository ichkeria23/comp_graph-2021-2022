from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window, key
from pyglet import clock
import numpy as np

# Проецирование
rot_x = 15
rot_y = 25
rot_z = 15

R = 30
h = R // 10
w = R + 2 * h
width = height = 400

textureIDs = (gl.GLuint * 6)()  # Массив идентификаторов (номеров) текстур
p = GL_TEXTURE_2D
tc = 1  # Число повторов текстуры

# Координаты вершин треугольника
v0 = (0.5 * w, 0.5 * w, 0)
v1 = (-0.5 * w, 0.5 * w, 0)
v2 = (-0.5 * w, -0.5 * w, 0)
v3 = (0.5 * w, -0.5 * w, 0)

t_x = v0[0]
t_y = v0[1]
change = False
char = '-'

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
    p3 = GL_REPEAT  # GL_REPEAT GL_CLAMP_TO_EDGE
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
    graphics.draw(4, GL_LINE_LOOP, ('v3f', v0 + v1 + v2 + v3), ('c3f', [0, 1, 0] * 4))


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


def mov_x(dt):
    global t_x, change, char
    if not change:
        if abs(t_x) <= 0.5 * w:
            if char == '-':
                t_x -= 0.1
            else:
                t_x += 0.1
        else:
            change = True
            if char == '-':
                t_x += 0.1
            else:
                t_x -= 0.1


def mov_y(dt):
    global t_y, change, char
    if change:
        if abs(t_y) <= 0.5 * w:
            if char == '-':
                t_y -= 0.1
            else:
                t_y += 0.1
        else:
            change = False
            if char == '-':
                t_y += 0.1
                char = '+'
            else:
                t_y -= 0.1
                char = '-'


clock.schedule_interval(mov_x, 0.01)
clock.schedule_interval(mov_y, 0.01)

window = Window(visible=True, width=width, height=height, resizable=True, caption="moving")
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
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    t_draw()
    glPopMatrix()
    glLoadIdentity()
    glTranslatef(t_x, t_y, v0[2])
    cube_draw()


app.run()