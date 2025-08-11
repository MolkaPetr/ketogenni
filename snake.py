import curses
import random


def main(stdscr):
    # Configure curses
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    # Initial snake position and direction
    sh, sw = stdscr.getmaxyx()
    x = sw // 4
    y = sh // 2
    snake = [
        [y, x],
        [y, x - 1],
        [y, x - 2],
    ]
    direction = curses.KEY_RIGHT

    # Initial food
    food = [
        random.randint(1, sh - 2),
        random.randint(1, sw - 2),
    ]
    stdscr.addch(food[0], food[1], curses.ACS_PI)

    while True:
        # Non-blocking input
        key = stdscr.getch()
        if key in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key

        # Calculate new head
        head = snake[0].copy()
        if direction == curses.KEY_RIGHT:
            head[1] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1

        # Collision with borders or self ends game
        if (
            head[0] in [0, sh] or
            head[1] in [0, sw] or
            head in snake
        ):
            break

        snake.insert(0, head)

        if head == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2),
                ]
                food = nf if nf not in snake else None
            stdscr.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(head[0], head[1], '#')


if __name__ == '__main__':
    curses.wrapper(main)
