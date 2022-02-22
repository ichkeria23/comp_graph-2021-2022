#
# Лицевая и нелицевая стороны треугольника
# Угол поворот в glRotatef меняется после нажатия на 1 (key._1) или 2 (key._2)
#
from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window, key

# Окно вывода
w = 400
h = 300
window = Window(visible=True, width=w, height=h,
                resizable=True, caption='PUSH_POP')
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPolygonMode(GL_FRONT, GL_FILL)  # Заливка лицевой стороны
glPolygonMode(GL_BACK, GL_LINE)  # Вывод нелицевой стороны в виде линей (ребер)
glPointSize(24)
push_pop = True
px = py = 0


@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-4, 4, -3, 3, -1, 1)  # Прямоугольное проецирование
    glLineWidth(12)
    # Аффинные преобразования выполняем в мировой система координат
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(180 * px, 1, 0, 0)  # Поворот вокруг оси X
    glRotatef(180 * py, 0, 1, 0)  # Поворот вокруг оси Y
    if push_pop:
        glPushMatrix()
        glLoadIdentity()  # делаем единичной
    graphics.draw(4, GL_LINES,
                  ('v2f', (-3.5, 0, 3.5, 0, 0, -2.5, 0, 2.5)),
                  ('c3f', (1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1)))
    graphics.draw(2, GL_POINTS,
                  ('v2f', (-2.5, -2.5, 2.5, 2.5)),
                  ('c3f', (1, 0, 1, 1, 1, 0)))
    glLineWidth(4)
    glColor3f(0, 1, 0)
    if push_pop:
        glPopMatrix()
    graphics.draw(3, GL_TRIANGLES, ('v2f', (-3, -1, 3, -2, 2, 1)))


@window.event
def on_key_press(symbol, modifiers):
    global px, py, push_pop
    if symbol == key._1:
        px = 1 - px
        py = 0
    elif symbol == key._2:
        px = 0
        py = 1 - py
    elif symbol == key._3:
        push_pop = not push_pop


app.run()
