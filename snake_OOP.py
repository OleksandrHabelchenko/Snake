from tkinter import *
import random
from playsound import playsound
import threading
from PIL import Image, ImageTk

# game settings
CELL = 20
WIDTH = 400
HEIGHT = 400
SPEED = 150

# create main window and canvas
root = Tk()
root.title("Snake Game | Score: 0")
canvas = Canvas(root, bg='black', width=WIDTH, height=HEIGHT)
canvas.pack()

# background music loop
music_playing = True

def play_music():
    while True:
        if music_playing:
            playsound('background.wav')

threading.Thread(target=play_music, daemon=True).start()

# load and resize background image
bg_image = Image.open('ground.jpg').resize((WIDTH, HEIGHT))
bg_foto = ImageTk.PhotoImage(bg_image)

class Game:
    def __init__(self):
        # initial snake position, direction, score and food
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = 'Right'
        self.score = 0
        self.food = [random.randrange(0, WIDTH, CELL),
                     random.randrange(0, HEIGHT, CELL)]
        self.running = True
        self.timer_id = None

    def draw(self):
        # clear canvas and redraw everything
        canvas.delete('all')
        canvas.create_image(0, 0, anchor='nw', image=bg_foto)

        # draw snake body
        for x, y in self.snake[1:]:
            canvas.create_rectangle(x+2, y+2, x+CELL-2, y+CELL-2,
                                    fill='#2d8a2d', outline='')

        # draw snake head
        hx, hy = self.snake[0]
        canvas.create_rectangle(hx+1, hy+1, hx+CELL-1,
                                hy+CELL-1, fill='#3cb83c', outline='')

        # eyes and tongue depend on direction
        if self.direction == 'Right':
            eyes = [(hx+13, hy+5), (hx+13, hy+13)]
            tongue_start = (hx+19, hy+9)
            tongue1 = (hx+24, hy+6)
            tongue2 = (hx+24, hy+12)
        elif self.direction == 'Left':
            eyes = [(hx+6, hy+5), (hx+6, hy+13)]
            tongue_start = (hx+1, hy+9)
            tongue1 = (hx-4, hy+6)
            tongue2 = (hx-4, hy+12)
        elif self.direction == 'Up':
            eyes = [(hx+5, hy+6), (hx+13, hy+6)]
            tongue_start = (hx+9, hy+1)
            tongue1 = (hx+6, hy-4)
            tongue2 = (hx+12, hy-4)
        elif self.direction == 'Down':
            eyes = [(hx+5, hy+13), (hx+13, hy+13)]
            tongue_start = (hx+9, hy+19)
            tongue1 = (hx+6, hy+24)
            tongue2 = (hx+12, hy+24)

        # draw eyes
        for ex, ey in eyes:
            canvas.create_oval(ex-3, ey-3, ex+3, ey+3,
                               fill='white', outline='')
            canvas.create_oval(ex-1, ey, ex+1, ey+2,
                               fill='#111', outline='')

        # draw tongue
        canvas.create_line(tongue_start[0], tongue_start[1],
                           tongue1[0], tongue1[1], fill='red', width=2)
        canvas.create_line(tongue_start[0], tongue_start[1],
                           tongue2[0], tongue2[1], fill='red', width=2)

        # draw food as yellow apple
        ax, ay = self.food
        canvas.create_oval(ax+2, ay+2, ax+CELL-2, ay+CELL-2,
                           fill="#f4ee49", outline='')
        canvas.create_rectangle(ax+9, ay, ax+11, ay+4,
                                fill='#5a3a1a', outline='')
        canvas.create_line(ax+10, ay+1, ax+16, ay-2,
                           fill='#2d8a2d', width=2)

    def move(self):
        # stop if game is over
        if not self.running:
            return

        # calculate new head position based on direction
        head = self.snake[0]
        if self.direction == 'Right':
            new_head = [head[0]+CELL, head[1]]
        elif self.direction == 'Left':
            new_head = [head[0]-CELL, head[1]]
        elif self.direction == 'Up':
            new_head = [head[0], head[1]-CELL]
        elif self.direction == 'Down':
            new_head = [head[0], head[1]+CELL]

        # check collision with walls or itself
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
            return

        # move snake forward
        self.snake.insert(0, new_head)

        # check if snake ate food
        if new_head == self.food:
            self.food[0] = random.randrange(0, WIDTH, CELL)
            self.food[1] = random.randrange(0, HEIGHT, CELL)
            self.score += 1
            root.title(f'Snake Game | Score: {self.score}')
            threading.Thread(target=lambda: playsound('food.mp3'),
                             daemon=True).start()
        else:
            # remove tail if no food eaten
            self.snake.pop()

        self.draw()
        # schedule next move
        self.timer_id = root.after(SPEED, self.move)

    def restart(self):
        # reset all game state to initial values
        global music_playing
        music_playing = True
        if self.timer_id:
            root.after_cancel(self.timer_id)
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.food = [random.randrange(0, WIDTH, CELL),
                     random.randrange(0, HEIGHT, CELL)]
        self.score = 0
        self.direction = 'Right'
        self.running = True
        self.timer_id = None
        root.title('Snake Game | Score: 0')
        self.draw()
        self.timer_id = root.after(100, self.move)

    def change_direction(self, event):
        # handle keyboard input
        if event.keysym in ('r', 'R') or event.keycode == 82:
            self.restart()
            return
        # prevent reversing direction
        if event.keysym == 'Right' and self.direction != 'Left':
            self.direction = 'Right'
        elif event.keysym == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        elif event.keysym == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.direction = 'Down'

# create game object and start
game = Game()
root.bind_all('<KeyPress>', game.change_direction)
game.move()
root.mainloop()



