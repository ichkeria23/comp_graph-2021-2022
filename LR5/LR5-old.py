import numpy as np
from pyglet import app, graphics, clock
from pyglet.gl import *
from pyglet.window import Window

n = 6
d = 15
wx, wy = 1.5 * d, 1.5 * d
width, height = int(30 * wx), int(30 * wy)
window = Window(visible=True, width=width, height=height, resizable=True, caption="LR5")


def to_c_float_Array(data):
    return (GLfloat * len(data))(*data)


light = 10
position_0 = (0, light + 10, 0)
position_0_fl = to_c_float_Array([0, light, 0, 0])
position_1 = (-light, 0, light)
position_1_fl = to_c_float_Array([-light, 0, light, 0])
mtClr_0 = [0.35, 0, 0.62, 0]
mtClr_0_fl = to_c_float_Array(mtClr_0)
clr_0 = (1, 1, 0)
clr_0_fv = to_c_float_Array(clr_0)
clr_1 = (1, 1, 1)
clr_1_fv = to_c_float_Array(clr_1)
ambient = to_c_float_Array([0.5, 0.5, 0.5, 1])

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)
glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
glEnable(GL_LIGHT0)
glEnable(GL_LIGHT1)
glEnable(GL_COLOR_MATERIAL)
# glEnable(GL_NORMALIZE)
glLightfv(GL_LIGHT0, GL_POSITION, position_0_fl)
glLightfv(GL_LIGHT1, GL_POSITION, position_1_fl)
glLightfv(GL_LIGHT0, GL_DIFFUSE, clr_0_fv)
glLightfv(GL_LIGHT1, GL_DIFFUSE, clr_1_fv)
glLightfv(GL_LIGHT0, GL_SPECULAR, mtClr_0_fl)
glLightfv(GL_LIGHT1, GL_SPECULAR, mtClr_0_fl)
glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, mtClr_0_fl)
glClearColor(0.4, 0.4, 0.4, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


# glPolygonMode(GL_FRONT, GL_LINE)
# glPolygonMode(GL_BACK, GL_LINE)


def ngon(xoff, yoff, zoff, r, vlist):
    for i in range(n):
        z = zoff + r * np.cos(2 * np.pi * i / n)
        x = xoff + r * np.sin(2 * np.pi * i / n)
        vlist.append((x, yoff, z))


vlist_top = []
vlist_bott = []

ngon(0, 10, 0, 10, vlist_top)
ngon(0, -10, 0, 10, vlist_bott)


def make_tuple(vl):
    v = ()
    for el in vl:
        v += el
    return v


def draw_bases():
    glColor3f(0.35, 0, 0.62)
    glNormal3f(0, 1, 0)
    graphics.draw(n, GL_POLYGON,
                  ('v3f', make_tuple(vlist_top)))
    glColor3f(0.35, 0, 0.62)
    glNormal3f(0, -1, 0)
    graphics.draw(n, GL_POLYGON,
                  ('v3f', make_tuple(vlist_bott)))


def draw_face():
    glColor3f(0.35, 0, 0.62)
    a = []
    b = []
    for i in range(n - 1):
        # a = [vlist_top[i - 1][0] - vlist_top[i][0], vlist_top[i - 1][1] - vlist_top[i][1],
        #      vlist_top[i - 1][2] - vlist_top[i][2]]
        # b = [vlist_bott[i][0] - vlist_top[i][0], vlist_bott[i][1] - vlist_top[i][1], vlist_bott[i][2] - vlist_top[i][2]]
        a = [vlist_top[i + 1][0] - vlist_top[i][0], vlist_top[i + 1][1] - vlist_top[i][1],
             vlist_top[i + 1][2] - vlist_top[i][2]]
        b = [vlist_top[i][0] - vlist_bott[i][0], vlist_top[i][1] - vlist_bott[i][1],
             vlist_top[i][2] - vlist_bott[i][2]]
        normal = np.cross(a, b)
        # normal = normal / np.linalg.norm(normal)
        glNormal3f(normal[0], normal[1], normal[2])
        graphics.draw(4, GL_QUADS,
                      ('v3f', (vlist_top[i] + vlist_top[i + 1] + vlist_bott[i + 1] + vlist_bott[i])))
    # a = [vlist_top[n - 1][0] - vlist_top[0][0], vlist_top[n - 1][1] - vlist_top[0][1],
    #      vlist_top[n - 1][2] - vlist_top[0][2]]
    # b = [vlist_bott[0][0] - vlist_top[0][0], vlist_bott[0][1] - vlist_top[0][1], vlist_bott[0][2] - vlist_top[0][2]]
    a = [vlist_top[0][0] - vlist_top[n - 1][0], vlist_top[0][1] - vlist_top[n - 1][1],
         vlist_top[0][2] - vlist_top[n - 1][2]]
    b = [vlist_top[n - 1][0] - vlist_bott[n - 1][0], vlist_top[n - 1][1] - vlist_bott[n - 1][1],
         vlist_top[n - 1][2] - vlist_bott[n - 1][2]]
    normal = np.cross(a, b)
    # normal = normal / np.linalg.norm(normal)
    glNormal3f(normal[0], normal[1], normal[2])
    graphics.draw(4, GL_QUADS,
                  ('v3f', (vlist_top[n - 1] + vlist_top[0] + vlist_bott[0] + vlist_bott[n - 1])))


n_rot, da = 1, 1


@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-wx, wx, -wy, wy, -20, 20)
    glRotatef(30, 1, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_bases()
    draw_face()

    glPointSize(16)
    glNormal3f(0, 1, 0)
    graphics.draw(1, GL_POINTS,
                  ('v3f', position_0), ('c3f', clr_0))
    glPushMatrix()
    glLoadIdentity()
    glRotatef(n_rot, 0, 1, 0)
    glNormal3f(1 / np.sqrt(2), 0, -1 / np.sqrt(2))
    graphics.draw(1, GL_POINTS,
                  ('v3f', position_1), ('c3f', clr_1))
    glPopMatrix()


def rotate(dt):
    global da, n_rot
    if n_rot == 0 or n_rot == 360:
        da = -da
    n_rot += da


clock.schedule_interval(rotate_prism, 0.05)

app.run()
