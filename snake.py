from tkinter import *

import random

CELL = 20
WIDTH = 400
HEIGHT = 400
SPEED = 150

root = Tk()
root.title("Snake Game | Score: 0")
canvas = Canvas(root, bg='black', width=WIDTH, height=HEIGHT)
canvas.pack()

snake = [[100, 100], [80, 100], [60, 100]]
direction = 'Right'
food = [random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)]
score = 0
running = True
timer_id = None

def draw():
    canvas.delete('all')
    for x, y in snake:
        canvas.create_rectangle(x, y, x + CELL, y + CELL,
                                fill='green')
    canvas.create_rectangle(food[0], food[1], food[0] + CELL,
                            food[1] + CELL, fill='yellow')

def move():
    global score, running, timer_id
    if not running:
        return
    head = snake[0]
    if direction == 'Right':
        new_head = [head[0] + CELL, head[1]]
    elif direction == 'Left':
        new_head = [head[0] - CELL, head[1]]
    elif direction == 'Up':
        new_head = [head[0], head[1] - CELL]
    elif direction == 'Down':
        new_head = [head[0], head[1] + CELL]

    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        running = False
        canvas.create_text(200, 200, text='GAME OVER',
                            fill='red', font=('Arial', 30))
        canvas.create_text(200, 240, text='Press R to restart',
                               fill='white', font=('Arial', 15))
        return

    snake.insert(0, new_head)
    if new_head == food:
        food[0] = random.randrange(0, WIDTH, CELL)
        food[1] = random.randrange(0, HEIGHT, CELL)
        score += 1
        root.title(f'Snake Game | Score: {score}')
    else:
        snake.pop()

    draw()
    timer_id = root.after(SPEED, move)

def full_restart():
    global snake, food, score, direction, running, timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    snake[:] = [[100, 100], [80, 100], [60, 100]]
    food[0] = random.randrange(0, WIDTH, CELL)
    food[1] = random.randrange(0, HEIGHT, CELL)
    score = 0
    direction = 'Right'
    root.title('Snake Game | Score: 0')
    draw()
    running = True
    timer_id = root.after(100, move)

def change_direction(event):
    global direction
    if event.keysym in ('r', 'R') or event.keycode == 82:
        full_restart()
        return
    if event.keysym == 'Right' and direction != 'Left':
        direction = 'Right'
    elif event.keysym == 'Left' and direction != 'Right':
        direction = 'Left'
    elif event.keysym == 'Up' and direction != 'Down':
        direction = 'Up'
    elif event.keysym == 'Down' and direction != 'Up':
        direction = 'Down'

root.bind_all('<KeyPress>', change_direction)
move()
root.mainloop()