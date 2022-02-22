#
# Лицевая и нелицевая стороны треугольника
# Угол поворот в glRotatef меняется после нажатия на 1 (key._1) или 2 (key._2)
#
from pyglet.gl import *
from pyglet import app
from pyglet.window import Window, key
# Координаты вершин полигона
v0 = (GLfloat * 3)(*[-3, -1, 0])
v1 = (GLfloat * 3)(*[3, -2, 0])
v2 = (GLfloat * 3)(*[2, 1, 0])
# glOrtho(-4, 4, -3, 3, -1, 1)
# Окно вывода
w = 400
h = 300
window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'FRONT_BACK')
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
gl.glLineWidth(4)
glPolygonMode(GL_FRONT, GL_FILL) # Заливка лицевой стороны
glPolygonMode(GL_BACK, GL_LINE) # Вывод нелицевой стороны в виде линей (ребер)
px = py = 0
@window.event
def on_draw():
    window.clear()
    # Аффинные преобразования выполняем в мировой система координат
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(180*px, 1, 0, 0) # Поворот вокруг оси X
    glRotatef(180*py, 0, 1, 0) # Поворот вокруг оси Y
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-4, 4, -3, 3, -8, 8) # Прямоугольное проецирование
    glColor3f(0, 1, 0)
    glBegin(GL_TRIANGLES)
    glVertex3fv(v0)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glEnd()
@window.event
def on_key_press(symbol, modifiers):
    global px, py
    if symbol == key._1:
        px = 1 - px
        py = 0
    elif symbol == key._2:
        px = 0
        py = 1 - py
app.run()

