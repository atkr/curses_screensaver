from __future__ import annotations

import curses
import random
import time


def _recolor() -> None:
    fg = random.randrange(0, curses.COLORS)
    # make sure it's not 16, which is the default color abd the same as the
    # background
    if fg == 16:
        fg = random.randrange(0, 16)
    curses.init_pair(1, fg, 16)


def c_main(stdscr: curses._CursesWindow) -> int:
    curses.start_color()
    curses.use_default_colors()

    curses.curs_set(0)  # no blinking cursor

    stdscr.nodelay(True)  # do not wait for user input (on get_wch())

    _recolor()
    stdscr.bkgd(' ', curses.color_pair(1))

    display_string = 'Hello World!'
    stdscr.addstr(display_string)
    x = y = 0
    dx = dy = 1

    while True:
        time.sleep(0.04)

        try:
            wch = stdscr.get_wch()
        except curses.error:
            pass  # this runs every loop iteration while no key is pressed
        else:
            # ensure we don't draw outside the window on resize
            if wch == curses.KEY_RESIZE:
                curses.update_lines_cols()
                x = min(curses.COLS - len(display_string), x)
                y = min(curses.LINES - 1, y)
            # if we get another key, exit
            else:
                return 0

        stdscr.move(y, 0)
        stdscr.clrtoeol()

        if x == curses.COLS - len(display_string):
            dx = -1
            _recolor()
        elif x == 0:
            dx = 1
            _recolor()

        if y == curses.LINES - 1:
            dy = -1
            _recolor()
        elif y == 0:
            dy = 1
            _recolor()

        x += dx
        y += dy

        # this is to avoid crashes when running addstr in the bottom right
        # corner of the screen
        try:
            stdscr.addstr(y, x, display_string)
        except curses.error:
            pass
        stdscr.refresh()


def main() -> int:
    return curses.wrapper(c_main)


if __name__ == '__main__':
    raise SystemExit(main())
