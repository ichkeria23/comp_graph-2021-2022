import random
import numpy as np
from pyglet.gl import *
from pyglet.window import Window
from pyglet import app


# функция для преобразования координаты (x, y)
def affine(c, x, y):
    x_ = x * c[0] + y * c[1] + c[4]
    y_ = x * c[2] + y * c[3] + c[5]
    return x_, y_


# коэффициенты преобразований
lst = [[0.1000, 0.00, 0.00, 0.16, 0.0, 0.0],
       [0.8500, 0.00, 0.00, 0.85, 0.0, 1.6],
       [-0.1667, -0.2887, 0.2887, -0.1667, 0.0, 1.6],
       [-0.1667, 0.2887, -0.2887, -0.1667, 0.0, 1.6]]

lst_eq = [0, 1, 2, 3]
lst_w = [0.01, 0.85, 0.07, 0.07]  # вероятности выбора того или иного столбца коэффициентов (весы)
lst_eq_n_1 = random.choices(lst_eq, weights=lst_w, k=1000)  # массив из индексов lst по весам (для выбора нач. точки)

w = 800
vp = np.full((w, w, 3), 255, dtype='uint8')

x0 = random.uniform(0, w) / 2  # выберем рандомное приближение для поиска нач. точки
y0 = random.uniform(0, w) / 2

# поиск начальной точки
xs = []
ys = []
j = 0
for i in lst_eq_n_1:
    j += 1
    x0, y0 = affine(lst[i], x0, y0)
    if j > 500:
        xs.append(x0)
        ys.append(y0)

# для установления зависимости для масштаба
print(max(xs), min(xs))
print(max(ys), min(ys))

vp[int(((x0 + 3) / 6) * 750)][int(((y0 + 0.5) / 11) * 750)] = [255, 0, 0]  # закрасим нач. точку

lst_eq_n_2 = random.choices(lst_eq, weights=lst_w, k=50000)  # массив из индексов lst по весам (для рисования)

# рисуем фрактал
for i in lst_eq_n_2:
    x0, y0 = affine(lst[i], x0, y0)
    vp[int(((x0 + 3) / 6) * 750)][int(((y0 + 0.5) / 11) * 750)] = [255, 0, 0]

vp = vp.flatten()
vp = (GLubyte * (w * w * 3))(*vp)
window = Window(visible=True, width=w, height=w, caption='38 - Fir_2')


@window.event
def on_draw():
    window.clear()
    glDrawPixels(w, w, GL_RGB, GL_UNSIGNED_BYTE, vp)


app.run()
