import pyglet
from pyglet import app, gl, graphics
from pyglet.window import Window, key


d = 12
d2 = 6
wx, wy = 1.5 * d, 1.2 * d2  # Параметры области визуализации
width, height = int(20 * wx), int(20 * wy)  # Размеры окна вывода
window = Window(visible = True, width = width, height = height,
                resizable = True, caption = 'Способы вывода многоугольника')
gl.glClearColor(0.1, 0.1, 0.1, 1.0)
gl.glClear(gl.GL_COLOR_BUFFER_BIT)
gl.glEnable(gl.GL_POINT_SMOOTH)
gl.glPointSize(10)
gl.glLineWidth(4)


@window.event
def on_draw():
    window.clear()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-wx, wx, -wy, wy, -1, 1)
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(0, 1, 0)
    gl.glVertex3f(-d, -d2, 0)
    gl.glVertex3f(-1, -d2, 0)
    gl.glVertex3f(-1, d2, 0)
    gl.glVertex3f(-d, d2, 0)
    gl.glEnd()
    graphics.draw(4, gl.GL_QUADS,
                  ('v2f', (1, -d2, 1, d2, d, d2, d, -d2)),
                  ('c3f', (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1)))


@window.event
def on_key_press(symbol, modifiers):
    mode_f = mode_b = None
    if symbol == key._1:
        mode_f = gl.GL_POINT
        mode_b = gl.GL_LINE
        shade_model = gl.GL_SMOOTH
    elif symbol == key._2:
        mode_f = gl.GL_LINE
        mode_b = gl.GL_POINT
        shade_model = gl.GL_SMOOTH
    elif symbol == key._3:
        mode_f = mode_b = gl.GL_FILL
        shade_model = gl.GL_FLAT
    elif symbol == key._4:
        mode_f = mode_b = gl.GL_FILL
        shade_model = gl.GL_SMOOTH
    if mode_f is not None:
        gl.glPolygonMode(gl.GL_FRONT, mode_f)
        gl.glPolygonMode(gl.GL_BACK, mode_b)
        gl.glShadeModel(shade_model)


app.run()