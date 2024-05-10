"""
On this module there are code to create terminal GUI and the program.
"""
from curses import wrapper, resize_term
from json import load

from fomodoro.utils import States, INFO_FILE
from fomodoro.stopwatch import prepare_stopwatch, run_stopwatch
from fomodoro.timer import prepare_timer, run_timer


def main(stdscr) -> None:
    """
    This function contains code to create terminal GUI and run the program.
    """
    resize_term(7, 40)

    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        info = load(info_file)

    if (info["stopwatch_state"] == States.WITHOUT_START.value
            or info["stopwatch_state"] == States.PAUSE.value):  # Stopwatch execute
        stopwatch_obj = prepare_stopwatch()

        stdscr.clear()  # Add instructions to screen
        stdscr.addstr(3, 5, "Instructions:")
        stdscr.addstr(4, 3, "- Press p to pause the stopwatch.")
        stdscr.addstr(5, 3, "- Press s to stop the stopwatch.")
        stdscr.refresh()

        run_stopwatch(stopwatch_obj)
    elif info["stopwatch_state"] == States.STOP.value:  # Timer execute
        timer_obj = prepare_timer()

        stdscr.clear()  # Add instructions to screen
        stdscr.addstr(3, 7, "Instructions:")
        stdscr.addstr(4, 5, "- Press p to pause the timer.")
        stdscr.refresh()

        run_timer(timer_obj)


FOMODORO = wrapper(main)
