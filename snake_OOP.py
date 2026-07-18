from tkinter import *                          # импортируем все виджеты tkinter
import random                                  # импортируем модуль случайных чисел
from playsound import playsound                # импортируем воспроизведение звука
import threading                               # импортируем потоки для фоновых задач
from PIL import Image, ImageTk                 # импортируем библиотеку для картинок
from db import Database, Leaderboard
from tkinter import simpledialog
from decouple import config

CELL = 20                                      # размер одной клетки в пикселях
WIDTH = 400                                    # ширина окна
HEIGHT = 400                                   # высота окна
SPEED = 150                                    # задержка между ходами в миллисекундах

root = Tk()                                    # создаём главное окно
root.title("Snake Game | Score: 0")
root.resizable(False, False)           # заголовок окна
canvas = Canvas(root, bg='black', width=WIDTH, height=HEIGHT)  # создаём холст для рисования
canvas.pack()                                  # размещаем холст в окне

music_playing = True                           # флаг управления фоновой музыкой

def play_music():                              # функция воспроизведения фоновой музыки
    while True:                                # бесконечный цикл
        if music_playing:                      # проверяем должна ли играть музыка
            playsound('background.wav')        # воспроизводим файл фоновой музыки

threading.Thread(target=play_music, daemon=True).start()  # запускаем музыку в фоновом потоке

bg_image = Image.open('ground.jpg').resize((WIDTH, HEIGHT))  # открываем и меняем размер фона
bg_foto = ImageTk.PhotoImage(bg_image)        # конвертируем картинку для tkinter

class Game:                                    # главный класс игры
    def __init__(self):                        # запускается один раз при создании объекта
        self.snake = [[100,100],[80,100],[60,100]]  # начальные позиции сегментов змейки
        self.direction = 'Right'               # начальное направление движения
        self.score = 0                         # начальный счёт
        self.food = [random.randrange(0, WIDTH, CELL),   # случайная позиция еды по x
                     random.randrange(0, HEIGHT, CELL)]  # случайная позиция еды по y
        self.running = True                    # игра запущена
        self.timer_id = None                   # хранит id таймера для отмены

    def draw(self):                            # рисует всё на холсте
        canvas.delete('all')                   # очищаем холст
        canvas.create_image(0, 0, anchor='nw', image=bg_foto)  # рисуем фон

        for x, y in self.snake[1:]:            # проходим по сегментам тела (без головы)
            canvas.create_rectangle(x+2, y+2, x+CELL-2, y+CELL-2,
                                    fill='#2d8a2d', outline='')  # рисуем сегмент тела

        hx, hy = self.snake[0]                 # получаем координаты головы
        canvas.create_rectangle(hx+1, hy+1, hx+CELL-1,
                                hy+CELL-1, fill='#3cb83c', outline='')  # рисуем голову

        if self.direction == 'Right':          # глаза и язык для направления вправо
            eyes = [(hx+13, hy+5), (hx+13, hy+13)]
            tongue_start = (hx+19, hy+9)
            tongue1 = (hx+24, hy+6)
            tongue2 = (hx+24, hy+12)
        elif self.direction == 'Left':         # глаза и язык для направления влево
            eyes = [(hx+6, hy+5), (hx+6, hy+13)]
            tongue_start = (hx+1, hy+9)
            tongue1 = (hx-4, hy+6)
            tongue2 = (hx-4, hy+12)
        elif self.direction == 'Up':           # глаза и язык для направления вверх
            eyes = [(hx+5, hy+6), (hx+13, hy+6)]
            tongue_start = (hx+9, hy+1)
            tongue1 = (hx+6, hy-4)
            tongue2 = (hx+12, hy-4)
        elif self.direction == 'Down':         # глаза и язык для направления вниз
            eyes = [(hx+5, hy+13), (hx+13, hy+13)]
            tongue_start = (hx+9, hy+19)
            tongue1 = (hx+6, hy+24)
            tongue2 = (hx+12, hy+24)

        for ex, ey in eyes:                    # рисуем каждый глаз
            canvas.create_oval(ex-3, ey-3, ex+3, ey+3,
                               fill='white', outline='')   # белая часть глаза
            canvas.create_oval(ex-1, ey, ex+1, ey+2,
                               fill='#111', outline='')    # зрачок

        canvas.create_line(tongue_start[0], tongue_start[1],
                           tongue1[0], tongue1[1], fill='red', width=2)  # первая линия языка
        canvas.create_line(tongue_start[0], tongue_start[1],
                           tongue2[0], tongue2[1], fill='red', width=2)  # вторая линия языка

        ax, ay = self.food                     # получаем координаты еды
        canvas.create_oval(ax+2, ay+2, ax+CELL-2, ay+CELL-2,
                           fill="#f4ee49", outline='')     # рисуем яблоко
        canvas.create_rectangle(ax+9, ay, ax+11, ay+4,
                                fill='#5a3a1a', outline='')  # рисуем черенок яблока
        canvas.create_line(ax+10, ay+1, ax+16, ay-2,
                           fill='#2d8a2d', width=2)        # рисуем листик яблока

    def move(self):                            # основная логика движения
        if not self.running:                   # если игра остановлена — выходим
            return
        head = self.snake[0]                   # берём голову змейки
        if self.direction == 'Right':          # считаем новую позицию головы вправо
            new_head = [head[0]+CELL, head[1]]
        elif self.direction == 'Left':         # считаем новую позицию головы влево
            new_head = [head[0]-CELL, head[1]]
        elif self.direction == 'Up':           # считаем новую позицию головы вверх
            new_head = [head[0], head[1]-CELL]
        elif self.direction == 'Down':         # считаем новую позицию головы вниз
            new_head = [head[0], head[1]+CELL]

        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake):
            self.running = False
            threading.Thread(target=lambda: playsound('game-over-music.wav'),
                      daemon=True).start()
            canvas.create_text(200, 200, text='GAME OVER',
                    fill='red', font=('Arial', 30))
            canvas.create_text(200, 240, text='Press R to restart',
                    fill='white', font=('Arial', 15))
            root.after(100, self.save_score)
            return                            

        self.snake.insert(0, new_head)         # добавляем новую голову в начало змейки

        if new_head == self.food:              # если съели еду
            self.food[0] = random.randrange(0, WIDTH, CELL)   # новая позиция еды по x
            self.food[1] = random.randrange(0, HEIGHT, CELL)  # новая позиция еды по y
            self.score += 1                    # увеличиваем счёт
            root.title(f'Snake Game | Score: {self.score}')   # обновляем заголовок
            threading.Thread(target=lambda: playsound('food.mp3'),
                             daemon=True).start()  # играем звук поедания
        else:
            self.snake.pop()                   # убираем хвост если еда не съедена

        self.draw()                            # перерисовываем всё
        self.timer_id = root.after(SPEED, self.move)  # через 150мс вызываем move снова

    def save_score(self):
        dialog = Toplevel(root)
        dialog.title("Game Over")
        dialog.geometry("350x150")
        dialog.resizable(False, False)

        # центрируем окно относительно основного окна игры
        dialog.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (350 // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (150 // 2)
        dialog.geometry(f"350x150+{x}+{y}")

        Label(dialog, text=f"You score: {self.score}", font=('Arial', 14)).pack(pady=10)
        Label(dialog, text="Enter Your Nickname:", font=('Arial', 12)).pack()

        entry = Entry(dialog, font=('Arial', 12))
        entry.pack(pady=10)
        entry.focus()

        def on_submit():
            nickname = entry.get()
            if nickname:
                leaderboard.add_score(nickname, self.score)
            dialog.destroy()

        Button(dialog, text="Save", command=on_submit).pack(pady=5)




    def restart(self):                         # сброс игры в начальное состояние
        if self.timer_id:                      # если таймер существует
            root.after_cancel(self.timer_id)   # отменяем его
        self.snake = [[100,100],[80,100],[60,100]]  # сбрасываем змейку
        self.food = [random.randrange(0, WIDTH, CELL),
                     random.randrange(0, HEIGHT, CELL)]  # новая случайная еда
        self.score = 0                         # обнуляем счёт
        self.direction = 'Right'               # начальное направление
        self.running = True                    # включаем игру
        self.timer_id = None                   # сбрасываем таймер
        root.title('Snake Game | Score: 0')   # сбрасываем заголовок
        self.draw()                            # рисуем начальное состояние
        self.timer_id = root.after(100, self.move)  # запускаем движение

    def change_direction(self, event):         # обработка нажатий клавиш
        if event.keysym in ('r', 'R') or event.keycode == 82:  # нажата R
            self.restart()                     # запускаем рестарт
            return
        if event.keysym == 'Right' and self.direction != 'Left':    # вправо
            self.direction = 'Right'
        elif event.keysym == 'Left' and self.direction != 'Right':  # влево
            self.direction = 'Left'
        elif event.keysym == 'Up' and self.direction != 'Down':     # вверх
            self.direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':     # вниз
            self.direction = 'Down'

db = Database(
    dbname=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    host=config('DB_HOST'),
    port=config('DB_PORT', cast=int)
)
leaderboard = Leaderboard(db)


game = Game()                                  # создаём объект игры
root.bind_all('<KeyPress>', game.change_direction)  # вешаем обработчик клавиш
game.move()                                    # запускаем игру
root.mainloop()                                # запускаем главный цикл окна

