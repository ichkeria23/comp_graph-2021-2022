from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
from pyglet import clock
import numpy as np

d, d1, d2 = 5, 10, 15
wx, wy = 1.5 * d2, 1.5 * d2
width, height = int(30 * wx), int(30 * wy)
window = Window(visible=True, width=width, height=height, resizable=True, caption='Chess_good')
glClearColor(0.4, 0.4, 0.4, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPointSize(24)

# glPolygonMode(GL_FRONT, GL_FILL)


def texInit():
    iWidth = iHeight = 64
    n = 3 * iWidth * iHeight
    img = np.zeros((iWidth, iHeight, 3), dtype='uint8')
    for i in range(iHeight):
        for j in range(iWidth):
            img[i, j, :] = (i & 16 ^ j & 16) * 255
    img = img.reshape(n)
    img = (GLubyte * n)(*img)
    p, r = GL_TEXTURE_2D, GL_RGB
    glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, GL_UNSIGNED_BYTE, img)
    glEnable(p)


texInit()
zv = -d2 / 2
v0, v1, v2, v3 = (-d2, d2, zv), (-d1, d1, 0), (d1, d1, 0), (d2, d2, zv)
# v01, v23 = (-d2, d1, 0), (d2, d1, 0)

# n = 0.1


@window.event
def on_draw():
    global n
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-wx, wx, -wy, wy, -20, 20)
    glRotatef(60, 1, 0, 0)
    graphics.draw(4, GL_QUADS, ('v3f', (v0 + v1 + v2 + v3)), ('t2f', (0, 0, 1 / (d2 - d1), 1, 1 - 1 / (d2 - d1) + 0.07, 1, 1, 0)))


# def izm(dt):
#     global n
#     n += 0.05
#
#
# clock.schedule_interval(izm, 1.5)

app.run()
