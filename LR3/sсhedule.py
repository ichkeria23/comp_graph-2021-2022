from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window
from pyglet import clock

# Окно вывода
w = 400
h = 300
window = Window(visible=True, width=w, height=h,
                resizable=True, caption='Schedule')
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPolygonMode(GL_FRONT, GL_FILL)  # Заливка лицевой стороны
glPolygonMode(GL_BACK, GL_LINE)  # Вывод нелицевой стороны в виде линей (ребер)
push_pop = 1
px = py = 0


def reverse_px(dt):
    global px
    px = 1 - px


def reverse_py(dt):
    global py
    py = 1 - py


def reverse_push_pop(dt):
    global push_pop
    push_pop = 1 - push_pop


clock.schedule_interval(reverse_px, 1.5)
clock.schedule_interval(reverse_py, 3.6)
clock.schedule_interval(reverse_push_pop, 7.5)
glLineWidth(4)
glPointSize(24)


@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-4, 4, -3, 3, -1, 1)  # Прямоугольное проецирование
    # Аффинные преобразования выполняем в мировой система координат
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(180 * px, 1, 0, 0)  # Поворот вокруг оси X
    glRotatef(180 * py, 0, 1, 0)  # Поворот вокруг оси Y
    if push_pop:
        glPushMatrix()
        glLoadIdentity()
    graphics.draw(2, GL_POINTS,
                  ('v2f', (-2.5, -2.5, 2.5, 2.5)),
                  ('c3f', (1, 0, 1, 1, 1, 0)))
    glColor3f(0, 1, 0)
    if push_pop: glPopMatrix()
    graphics.draw(3, GL_TRIANGLES, ('v2f', (-3, -1, 3, -2, 2, 1)))


app.run()
