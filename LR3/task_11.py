# Вывести 2-d сцену с квадратом в 3-м квадранте и осями координат.
# После нажатия на 1 квадрат перемещается в 1-й квадрант,
# а при повторном нажатии на 1 - возвращается на место.
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
glPolygonMode(GL_FRONT, GL_LINE)  # Заливка лицевой стороны
pz = 0


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
    glRotatef(180 * pz, 0, 0, 1)  # Поворот вокруг оси Z
    glPushMatrix()
    glLoadIdentity()  # делаем единичной
    graphics.draw(4, GL_LINES,
                  ('v2f', (-3.5, 0, 3.5, 0, 0, -2.5, 0, 2.5)),
                  ('c3f', (1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1)))
    glLineWidth(1)
    glColor3f(0, 1, 0)
    glPopMatrix()
    graphics.draw(4, GL_QUADS,
                  ('v2f', (-1, -1, -2, -1, -2, -2, -1, -2)),
                  ('c3f', (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0)))


@window.event
def on_key_press(symbol, modifiers):
    global pz
    if symbol == key._1:
        pz = 1 - pz


app.run()