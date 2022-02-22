import numpy as np
from numpy.random import randint
from pyglet import app, graphics, clock
from pyglet.gl import *
from pyglet.window import Window, key

n = 9
d = 15
w = 1.5 * d
width, height = int(30 * w), int(30 * w)
window = Window(visible=True, width=width, height=height, resizable=True, caption="LR5")

bases = True
normalize = False
normalview = True
normaltofaces = True
move = False
lightposition = False
figureposition = False
rot_x, rot_y, rot_z = 0, 0, 0


def to_c_float_Array(data):
    return (GLfloat * len(data))(*data)


mtClr_0 = [0.35, 0, 0.62, 0]
mtClr_0_fl = to_c_float_Array(mtClr_0)
light = 20
x = 0
z = light
dx = 0.1
change = False
char = '+'
position_0 = (0, light, 0)
position_0_fl = to_c_float_Array([0, light, 0, 0])
clr_0 = (1, 1, 0)
clr_0_fl = to_c_float_Array(clr_0)
position_1 = (x, 0, z)
position_1_fl = to_c_float_Array([x, 0, z, 0])
clr_1 = (1, 1, 1)
clr_1_fl = to_c_float_Array(clr_1)


# def make_tuple(vl):
#     tup = ()
#     for elem in vl:
#         tup += elem
#     return tup


glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
# glEnable(GL_NORMALIZE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, position_0_fl)
# glLightfv(GL_LIGHT0, GL_AMBIENT, clr_0_fl)
glLightfv(GL_LIGHT0, GL_DIFFUSE, clr_0_fl)

glEnable(GL_LIGHT1)
glLightfv(GL_LIGHT1, GL_POSITION, position_1_fl)
glLightfv(GL_LIGHT1, GL_DIFFUSE, clr_1_fl)
# glLightfv(GL_LIGHT1, GL_AMBIENT, clr_1_fl)

glColorMaterial(GL_FRONT, GL_DIFFUSE)

glClearColor(0.4, 0.4, 0.4, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

vlist_top = []  # верхние точки призмы
vlist_bott = []  # нижние точки призмы
vlist_top_vectors = []
vlist_bott_vectors = []
vlist_top_normals = []
vlist_bott_normals = []
vlist_top_normals_points = []
vlist_bott_normals_points = []


def ngon_dots(xoff, yoff, zoff, r, vlist):
    global n
    for i in range(n):
        x_ = xoff + r * np.sin(2 * np.pi * i / n)
        z_ = zoff + r * np.cos(2 * np.pi * i / n)
        vlist.append((x_, yoff, z_))


def memorize_vectors_to_calculate_normals():
    global n, vlist_top, vlist_bott, vlist_top_vectors, vlist_bott_vectors
    a, b, c, d_, e, f = [], [], [], [], [], []
    for i in range(n):
        if i == 0:
            a = [vlist_top[n - 1][0] - vlist_top[0][0], vlist_top[n - 1][1] - vlist_top[0][1],
                 vlist_top[n - 1][2] - vlist_top[0][2]]
            b = [vlist_bott[0][0] - vlist_top[0][0], vlist_bott[0][1] - vlist_top[0][1],
                 vlist_bott[0][2] - vlist_top[0][2]]
            c = [vlist_top[1][0] - vlist_top[0][0], vlist_top[1][1] - vlist_top[0][1],
                 vlist_top[1][2] - vlist_top[0][2]]
            d_ = [vlist_bott[n - 1][0] - vlist_bott[0][0], vlist_bott[n - 1][1] - vlist_bott[0][1],
                  vlist_bott[n - 1][2] - vlist_bott[0][2]]
            e = [vlist_top[0][0] - vlist_bott[0][0], vlist_top[0][1] - vlist_bott[0][1],
                 vlist_top[0][2] - vlist_bott[0][2]]
            f = [vlist_bott[1][0] - vlist_bott[0][0], vlist_bott[1][1] - vlist_bott[0][1],
                 vlist_bott[1][2] - vlist_bott[0][2]]
        elif i == n - 1:
            a = [vlist_top[n - 2][0] - vlist_top[n - 1][0], vlist_top[n - 2][1] - vlist_top[n - 1][1],
                 vlist_top[n - 2][2] - vlist_top[n - 1][2]]
            b = [vlist_bott[n - 1][0] - vlist_top[n - 1][0], vlist_bott[n - 1][1] - vlist_top[n - 1][1],
                 vlist_bott[n - 1][2] - vlist_top[n - 1][2]]
            c = [vlist_top[0][0] - vlist_top[n - 1][0], vlist_top[0][1] - vlist_top[n - 1][1],
                 vlist_top[0][2] - vlist_top[n - 1][2]]
            d_ = [vlist_bott[n - 2][0] - vlist_bott[n - 1][0], vlist_bott[n - 2][1] - vlist_bott[n - 1][1],
                  vlist_bott[n - 2][2] - vlist_bott[n - 1][2]]
            e = [vlist_top[n - 1][0] - vlist_bott[n - 1][0], vlist_top[n - 1][1] - vlist_bott[n - 1][1],
                 vlist_top[n - 1][2] - vlist_bott[n - 1][2]]
            f = [vlist_bott[0][0] - vlist_bott[n - 1][0], vlist_bott[0][1] - vlist_bott[n - 1][1],
                 vlist_bott[0][2] - vlist_bott[n - 1][2]]
        else:
            a = [vlist_top[i - 1][0] - vlist_top[i][0], vlist_top[i - 1][1] - vlist_top[i][1],
                 vlist_top[i - 1][2] - vlist_top[i][2]]
            b = [vlist_bott[i][0] - vlist_top[i][0], vlist_bott[i][1] - vlist_top[i][1],
                 vlist_bott[i][2] - vlist_top[i][2]]
            c = [vlist_top[i + 1][0] - vlist_top[i][0], vlist_top[i + 1][1] - vlist_top[i][1],
                 vlist_top[i + 1][2] - vlist_top[i][2]]
            d_ = [vlist_bott[i - 1][0] - vlist_bott[i][0], vlist_bott[i - 1][1] - vlist_bott[i][1],
                  vlist_bott[i - 1][2] - vlist_bott[i][2]]
            e = [vlist_top[i][0] - vlist_bott[i][0], vlist_top[i][1] - vlist_bott[i][1],
                 vlist_top[i][2] - vlist_bott[i][2]]
            f = [vlist_bott[i + 1][0] - vlist_bott[i][0], vlist_bott[i + 1][1] - vlist_bott[i][1],
                 vlist_bott[i + 1][2] - vlist_bott[i][2]]
        vlist_top_vectors.append((a, b, c))
        vlist_bott_vectors.append((d_, e, f))


def calculate_normals():
    global n, vlist_top_normals, vlist_bott_normals, vlist_top_normals_points, vlist_bott_normals_points, \
        vlist_top_vectors, vlist_bott_vectors, vlist_top, vlist_bott, bases, normalize
    n1, n2, n3, vn = [], [], [], []
    for i in range(n):
        n1 = np.cross(vlist_top_vectors[i][0], vlist_top_vectors[i][1])
        n2 = np.cross(vlist_top_vectors[i][1], vlist_top_vectors[i][2])
        vn = np.array([n1[0] + n2[0], n1[1], n1[2] + n2[2]])
        if bases:
            n3 = np.cross(vlist_top_vectors[i][2], vlist_top_vectors[i][0])
            vn = np.array([vn[0] + n3[0], vn[1] + n3[1], vn[2] + n3[2]])
        if normalize:
            n1 = n1 / np.linalg.norm(n1)
            n2 = n2 / np.linalg.norm(n2)
            vn = vn / np.linalg.norm(vn)
        vlist_top_normals.append((n1, n2, vn))
        vlist_top_normals_points.append(((n1[0] + vlist_top[i][0], n1[1] + vlist_top[i][1], n1[2] + vlist_top[i][2]),
                                         (n2[0] + vlist_top[i][0], n2[1] + vlist_top[i][1], n2[2] + vlist_top[i][2]),
                                         (vn[0] + vlist_top[i][0], vn[1] + vlist_top[i][1], vn[2] + vlist_top[i][2])))
        n1 = np.cross(vlist_bott_vectors[i][1], vlist_bott_vectors[i][0])
        n2 = np.cross(vlist_bott_vectors[i][2], vlist_bott_vectors[i][1])
        vn = np.array([n1[0] + n2[0], n1[1], n1[2] + n2[2]])
        if bases:
            n3 = np.cross(vlist_bott_vectors[i][0], vlist_bott_vectors[i][2])
            vn = np.array([vn[0] + n3[0], vn[1] + n3[1], vn[2] + n3[2]])
        if normalize:
            n1 = n1 / np.linalg.norm(n1)
            n2 = n2 / np.linalg.norm(n2)
            vn = vn / np.linalg.norm(vn)
        vlist_bott_normals.append((n1, n2, vn))
        vlist_bott_normals_points.append(
            ((n1[0] + vlist_bott[i][0], n1[1] + vlist_bott[i][1], n1[2] + vlist_bott[i][2]),
             (n2[0] + vlist_bott[i][0], n2[1] + vlist_bott[i][1], n2[2] + vlist_bott[i][2]),
             (vn[0] + vlist_bott[i][0], vn[1] + vlist_bott[i][1], vn[2] + vlist_bott[i][2])))


def draw_faces():
    global n, normaltofaces, vlist_top, vlist_bott, vlist_top_normals, vlist_bott_normals
    glColor3fv(mtClr_0_fl)
    for i in range(n - 1):
        if normaltofaces:
            glNormal3f(vlist_top_normals[i][1][0], vlist_top_normals[i][1][1], vlist_top_normals[i][1][2])
        glBegin(GL_QUADS)
        glNormal3f(vlist_top_normals[i][2][0], vlist_top_normals[i][2][1], vlist_top_normals[i][2][2])
        glVertex3f(vlist_top[i][0], vlist_top[i][1], vlist_top[i][2])
        glNormal3f(vlist_top_normals[i + 1][2][0], vlist_top_normals[i + 1][2][1], vlist_top_normals[i + 1][2][2])
        glVertex3f(vlist_top[i + 1][0], vlist_top[i + 1][1], vlist_top[i + 1][2])
        glNormal3f(vlist_bott_normals[i + 1][2][0], vlist_bott_normals[i + 1][2][1], vlist_bott_normals[i + 1][2][2])
        glVertex3f(vlist_bott[i + 1][0], vlist_bott[i + 1][1], vlist_bott[i + 1][2])
        glNormal3f(vlist_bott_normals[i][2][0], vlist_bott_normals[i][2][1], vlist_bott_normals[i][2][2])
        glVertex3f(vlist_bott[i][0], vlist_bott[i][1], vlist_bott[i][2])
        glEnd()

    if normaltofaces:
        glNormal3f(vlist_top_normals[n - 1][1][0], vlist_top_normals[n - 1][1][1], vlist_top_normals[n - 1][1][2])
    glBegin(GL_QUADS)
    glNormal3f(vlist_top_normals[n - 1][2][0], vlist_top_normals[n - 1][2][1], vlist_top_normals[n - 1][2][2])
    glVertex3f(vlist_top[n - 1][0], vlist_top[n - 1][1], vlist_top[n - 1][2])
    glNormal3f(vlist_top_normals[0][2][0], vlist_top_normals[0][2][1], vlist_top_normals[0][2][2])
    glVertex3f(vlist_top[0][0], vlist_top[0][1], vlist_top[0][2])
    glNormal3f(vlist_bott_normals[0][2][0], vlist_bott_normals[0][2][1], vlist_bott_normals[0][2][2])
    glVertex3f(vlist_bott[0][0], vlist_bott[0][1], vlist_bott[0][2])
    glNormal3f(vlist_bott_normals[n - 1][2][0], vlist_bott_normals[n - 1][2][1], vlist_bott_normals[n - 1][2][2])
    glVertex3f(vlist_bott[n - 1][0], vlist_bott[n - 1][1], vlist_bott[n - 1][2])
    glEnd()


def draw_lights():
    glPointSize(16)
    glEnable(GL_POINT_SMOOTH)
    # glNormal3f(0, 1, 0)
    graphics.draw(1, GL_POINTS,
                  ('v3f', position_0), ('c3f', clr_0))
    # glNormal3f(0, 0, -1)
    graphics.draw(1, GL_POINTS,
                  ('v3f', position_1), ('c3f', clr_1))


def draw_axes():
    global w
    glLineWidth(5)
    v0 = (0, 0, 0)
    c0 = (1, 1, 0)
    graphics.draw(2, GL_LINES,
                  ('v3f', (v0 + (w, 0, 0))), ('c3f', (c0 + (1, 0, 0))))
    graphics.draw(2, GL_LINES,
                  ('v3f', (v0 + (0, w, 0))), ('c3f', (c0 + (0, 1, 0))))
    graphics.draw(2, GL_LINES,
                  ('v3f', (v0 + (0, 0, w))), ('c3f', (c0 + (0, 0, 1))))


def draw_bases():
    global normalize, n, vlist_top, vlist_bott
    glColor3fv(mtClr_0_fl)
    if normalize:
        glNormal3f(0, 1, 0)
    else:
        glNormal3f(0, 3, 0)

    # graphics.draw(n, GL_POLYGON, ('v3f', # make_tuple(vlist_top)))
    #                               (vlist_top[0] + vlist_top[1] + vlist_top[2] + vlist_top[3] + vlist_top[4] + vlist_top[5])))
    glBegin(GL_POLYGON)
    for i in range(n):
        glVertex3f(vlist_top[i][0], vlist_top[i][1], vlist_top[i][2])
    glEnd()
    # glColor3fv(mtClr_0_fl)
    if normalize:
        glNormal3f(0, -1, 0)
    else:
        glNormal3f(0, -3, 0)
    # graphics.draw(n, GL_POLYGON, ('v3f', #  make_tuple(vlist_bott)))
    #                              vlist_bott[0] + vlist_bott[1] + vlist_bott[2] + vlist_bott[3] + vlist_bott[4] + vlist_bott[5]))
    glBegin(GL_POLYGON)
    for i in range(n):
        glVertex3f(vlist_bott[i][0], vlist_bott[i][1], vlist_bott[i][2])
    glEnd()


def draw_normals():
    global n, normaltofaces, vlist_top, vlist_bott, \
        vlist_top_normals_points, vlist_bott_normals_points
    c0 = (1, 0, 0)
    c1 = (1, 1, 1)
    glLineWidth(1)
    for i in range(n):
        if normaltofaces:
            graphics.draw(2, GL_LINES,
                          ('v3f', (vlist_top[i] + vlist_top_normals_points[i][0])), ('c3f', (c0 + c0)))
            graphics.draw(2, GL_LINES,
                          ('v3f', (vlist_top[i] + vlist_top_normals_points[i][1])), ('c3f', (c0 + c0)))
            graphics.draw(2, GL_LINES,
                          ('v3f', (vlist_bott[i] + vlist_bott_normals_points[i][0])), ('c3f', (c0 + c0)))
            graphics.draw(2, GL_LINES,
                          ('v3f', (vlist_bott[i] + vlist_bott_normals_points[i][1])), ('c3f', (c0 + c0)))
        graphics.draw(2, GL_LINES,
                      ('v3f', (vlist_top[i] + vlist_top_normals_points[i][2])), ('c3f', (c1 + c1)))
        graphics.draw(2, GL_LINES,
                      ('v3f', (vlist_bott[i] + vlist_bott_normals_points[i][2])), ('c3f', (c1 + c1)))


def draw_figure():
    global vlist_top, vlist_bott, bases, normalview
    ngon_dots(0, 15, 0, 6, vlist_top)
    ngon_dots(0, 0, 0, 6, vlist_bott)
    memorize_vectors_to_calculate_normals()
    calculate_normals()
    if bases:
        draw_bases()
    draw_faces()
    if normalview:
        draw_normals()


@window.event
def on_draw():
    global w, rot_x, rot_y, rot_z
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-w, w, -w, w, -20, 20)
    glRotatef(30, 1, 0, 0)
    glRotatef(-30, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_axes()
    glPushMatrix()
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)
    draw_figure()
    glPopMatrix()
    draw_lights()


@window.event
def on_key_press(symbol, modifiers):
    global bases, normalize, normalview, position_0, position_0_fl, \
        normaltofaces, move, lightposition, figureposition, light, rot_x, rot_y, rot_z, \
        vlist_top, vlist_bott, vlist_top_vectors, vlist_top_normals, \
        vlist_bott_vectors, vlist_bott_normals, vlist_top_normals_points, vlist_bott_normals_points
    vlist_top.clear()
    vlist_bott.clear()
    vlist_top_vectors.clear()
    vlist_bott_vectors.clear()
    vlist_top_normals.clear()
    vlist_bott_normals.clear()
    vlist_top_normals_points.clear()
    vlist_bott_normals_points.clear()
    if symbol == key._1:
        bases = not bases
    elif symbol == key._2:
        normaltofaces = not normaltofaces
    elif symbol == key._3:
        normalview = not normalview
    elif symbol == key._4:
        if glIsEnabled(GL_DEPTH_TEST) == GL_TRUE:
            glDisable(GL_DEPTH_TEST)
        else:
            glEnable(GL_DEPTH_TEST)
    elif symbol == key._5:
        if glIsEnabled(GL_CULL_FACE) == GL_TRUE:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)
    elif symbol == key._6:
        if glIsEnabled(GL_LIGHT0) == GL_TRUE:
            glDisable(GL_LIGHT0)
        else:
            glEnable(GL_LIGHT0)
    elif symbol == key._7:
        normalize = not normalize
    elif symbol == key._8:
        if glIsEnabled(GL_NORMALIZE) == GL_TRUE:
            glDisable(GL_NORMALIZE)
        else:
            glEnable(GL_NORMALIZE)
    elif symbol == key._9:
        if glIsEnabled(GL_LIGHTING) == GL_TRUE:
            glDisable(GL_LIGHTING)
        else:
            glEnable(GL_LIGHTING)
    elif symbol == key._0:
        if glIsEnabled(GL_COLOR_MATERIAL) == GL_TRUE:
            glDisable(GL_COLOR_MATERIAL)
        else:
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT, GL_DIFFUSE)
    elif symbol == key.Q:
        move = not move
    elif symbol == key.W:
        lightposition = not lightposition
        if not lightposition:
            position_0 = (0, light, 0)
            position_0_fl = to_c_float_Array([0, light, 0, 0])
            glLightfv(GL_LIGHT0, GL_POSITION, position_0_fl)
        else:
            position_0 = (randint(-20, 21), randint(-20, 21), randint(-20, 21))
            position_0_fl = to_c_float_Array([position_0[0], position_0[1], position_0[2], 0])
            glLightfv(GL_LIGHT0, GL_POSITION, position_0_fl)
    elif symbol == key.E:
        figureposition = not figureposition
        if not figureposition:
            rot_x, rot_y, rot_z = 0, 0, 0
        else:
            rot_x, rot_y, rot_z = randint(0, 181), randint(0, 181), randint(0, 181)
    elif symbol == key.R:
        if glIsEnabled(GL_LIGHT1) == GL_TRUE:
            glDisable(GL_LIGHT1)
        else:
            glEnable(GL_LIGHT1)


def mov_x(dt):
    global light, x, z, position_1, position_1_fl, change, char, move, dx
    if move:
        if change:
            if abs(x) <= light:
                if char == '-':
                    x -= dx
                else:
                    x += dx
            else:
                change = False
                if char == '-':
                    x += dx
                    char = '+'
                else:
                    x -= dx
                    char = '-'
        position_1 = (x, 0, z)
        position_1_fl = to_c_float_Array([x, 0, z, 0])
        glLightfv(GL_LIGHT1, GL_POSITION, position_1_fl)


def mov_z(dt):
    global light, x, z, position_1, position_1_fl, change, char, move, dx
    if move:
        if not change:
            if abs(z) <= light:
                if char == '-':
                    z -= dx
                else:
                    z += dx
            else:
                change = True
                if char == '-':
                    z += dx
                else:
                    z -= dx
        position_1 = (x, 0, z)
        position_1_fl = to_c_float_Array([x, 0, z, 0])
        glLightfv(GL_LIGHT1, GL_POSITION, position_1_fl)


clock.schedule_interval(mov_x, 0.01)
clock.schedule_interval(mov_z, 0.01)

app.run()