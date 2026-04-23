import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np


def f(x):
    '''Функция может быть изменена например return x'''
    return x ** 2

# границы отрезка, также могут быть изменены
a, b = 0, 1
x_dense = np.linspace(a, b, 1000)
y_dense = f(x_dense)

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2) # место расположения слайдера

# сам график
ax.plot(x_dense, y_dense, 'k-', linewidth=2, label=f'$f(x) = 1/x$')
ax.set_xlim(a, b)
ax.set_ylim(0, f(b) + 0.0001) # в заисимости от того монотонно возр или убыв функция меняйте f(b) на f(a) иначе график не войдет в границу
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Верхние и нижние суммы Дарбу')
ax.grid(True)

# прямоугольники upper - верхний интеграл, lower - нижние интеграл, а yellow - чтото среднее np.average() 
upper_rects = ax.bar([], [], width=0, align='edge', alpha=0.5, color='red', edgecolor='darkred', label='Верхняя сумма')
yellow_rects = ax.bar([], [], width=0, align='edge', alpha=0.5, color='yellow', label='Что-то среднее между')
lower_rects = ax.bar([], [], width=0, align='edge', alpha=0.5, color='blue', edgecolor='darkblue', label='Нижняя сумма')

# отображение сумм и их разности через текст
text_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.legend(loc='upper right')

# ось для слайдера 
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, "Шаг дискретизации Δ(5 - 100)", valmin=5, valmax=100, valinit=5, valstep=1)

def update(val):
    global upper_rects, lower_rects, yellow_rects
    
    delta = int(slider.val)
    
    # равномерно разбиваем
    x_edges = np.linspace(a, b, delta + 1)
    dx = (b - a) / delta 
    
    lower_heights = np.zeros(delta)
    upper_heights = np.zeros(delta)
    yellow_heights = np.zeros(delta)
    
    
    #для каждого частичного сегмента [x_i_1, x_i_2] найдем min & max 
    for i in range(delta):
        x_i_1 = x_edges[i]
        x_i_2 = x_edges[i + 1]
        x_sub = np.linspace(x_i_1, x_i_2, 100)
        y_sub = f(x_sub)
        
        lower_heights[i] = np.min(y_sub)
        upper_heights[i] = np.max(y_sub)
        yellow_heights[i] = np.average(y_sub)
        
    # очистка старых прямоугольников если они были
    for rect in upper_rects: rect.remove()
    for rect in lower_rects: rect.remove()
    for rect in yellow_rects: rect.remove()
    
    # апдейт отрисовки
    upper_rects_new = ax.bar(x_edges[:-1], upper_heights, width=dx, align='edge', alpha=0.5, color='red', edgecolor='darkred', label='Верхняя сумма')
    yellow_rects_new = ax.bar(x_edges[:-1], yellow_heights, width=dx, align='edge', alpha=0.5, color='yellow', label='Что-то среднее между')
    lower_rects_new = ax.bar(x_edges[:-1], lower_heights, width=dx, align='edge', alpha=0.5, color='blue', edgecolor='darkblue', label='Нижняя сумма')
    
    # обновляем ссылки глобально для следующего апдейта
    upper_rects = upper_rects_new
    yellow_rects = yellow_rects_new
    lower_rects = lower_rects_new
    
    # вычисляем суммы
    S_upper = np.sum(upper_heights * dx)
    S_lower = np.sum(lower_heights * dx)
    diff = S_upper - S_lower
    # апдейт текста    
    text_info.set_text(f'Верхняя сумма = {S_upper:.3f}\nНижняя сумма = {S_lower:.3f}\nРазность = {diff:.3f}')
    
    fig.canvas.draw_idle()


update(slider.val)
# подключили слайдер
slider.on_changed(update)

plt.show()