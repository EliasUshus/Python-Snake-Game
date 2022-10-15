import curses 
from random import randint
import os

#constants
WINDOW_WIDTH = 60  # number of columns of window box 
WINDOW_HEIGHT = 20 # number of rows of window box 

# Choose difficulty START
print("Difficulties: Hard, Medium or Easy")
difficulty = ""
difficulty = input("\nChoose difficulty: ").lower()

speed = 0

if difficulty == 'hard':
    speed = 70
elif difficulty == 'easy':
    speed = 150
else:
    speed = 100
    difficulty = 'medium'
# Choose difficulty END

running = "yes"
while running == "yes" or running == "y":
    curses.initscr()
    win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0) # rows, columns
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1) # -1

    # snake and food
    snake = [(4, 4), (4, 3), (4, 2)]
    food = (6, 6)
    win.addch(food[0], food[1], '#')
    
    # game logic
    score = 0
    ESC = 27
    key = curses.KEY_RIGHT

    while key != ESC:
        win.addstr(0, 2, 'Score: ' + str(score) + ' ' + 'Difficulty: ' + str(difficulty))
        win.timeout(speed - (len(snake)) // 5 + len(snake)//10 % 120) # increase speed alt efter difficulty

        prev_key = key
        event = win.getch()
        key = event if event != -1 else prev_key

        if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
            key = prev_key

        # calculate the next coordinates
        y = snake[0][0]
        x = snake[0][1]
        if key == curses.KEY_DOWN:
            y += 1
        if key == curses.KEY_UP:
            y -= 1
        if key == curses.KEY_LEFT:
            x -= 1
        if key == curses.KEY_RIGHT:
            x += 1
        snake.insert(0, (y, x)) # append O(n)

        # check if we hit the border
        if y == 0: break
        if y == WINDOW_HEIGHT-1: break
        if x == 0: break
        if x == WINDOW_WIDTH -1: break

        # if snake runs over itself
        if snake[0] in snake[1:]: break

        if snake[0] == food:
            # eat the food
            score += 1
            food = ()
            while food == ():
                food = (randint(1,WINDOW_HEIGHT-2), randint(1,WINDOW_WIDTH -2))
                if food in snake:
                    food = ()
            win.addch(food[0], food[1], '#')
        else:
            # move snake
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '*')

    curses.endwin()
    os.system('cls')

    f = open("highscore.txt", "r")
    highscore = int(f.read())
    f.close()

    if highscore < score:
        f = open("highscore.txt", "w")
        f.write(f"{score}")
        f.close()
        print(f"You got a new highscore! {score}")
    else:
        print(f"Try Again! Your highscore is {highscore}")

    print(f"Your score was {score}")
    running = input("\nPlay Again? (y/n)").lower()