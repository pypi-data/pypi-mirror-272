"""
This module has all code related to timer.
"""
from json import load, dump
from time import sleep
from winsound import PlaySound, SND_FILENAME
import curses

from fomodoro.utils import States, INFO_FILE, BELL_SOUND_FILE, format_seconds
from fomodoro.stats import add_timer_record


class Timer():
    """
    To can manipulate the timer easiest by functions.
    """
    def __init__(self) -> None:
        self.state = States.WITHOUT_START
        self.break_time_in_seconds: int = 0

    def start(self):
        self.state = States.START

    def pause(self):
        self.state = States.PAUSE

    def stop(self):
        self.state = States.STOP


timer_obj = Timer()


def prepare_timer() -> Timer:
    """
    This function prepare the timer obj to run timer.
    """
    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        info: dict = load(info_file)

    timer_obj.start()
    if info["timer_state"] == States.WITHOUT_START.value:
        amount_of_seconds_for_the_timer: float = round(info["elapsed_seconds"] / 5)
        add_timer_record(amount_of_seconds_for_the_timer)
    else:
        amount_of_seconds_for_the_timer: float = info["leftover_break_time_in_seconds"]

    timer_obj.break_time_in_seconds = int(amount_of_seconds_for_the_timer)

    return timer_obj


def run_timer(timer: Timer):
    """
    This function run timer.
    """
    time_window = curses.newwin(1, 9, 1, 16)

    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        info: dict = load(info_file)

    while timer.state is States.START:
        sleep(1.0)
        if timer.break_time_in_seconds > 0:
            timer.break_time_in_seconds -= 1
        else:
            timer.stop()

            info.update({"timer_state": States.WITHOUT_START.value})
            info.update({"leftover_break_time_in_seconds": 0})
            info.update({"elapsed_seconds": 0})
            info.update({"stopwatch_state": States.WITHOUT_START.value})
            with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                dump(info, info_file, indent=2)

            PlaySound(BELL_SOUND_FILE, SND_FILENAME)

        time_window.nodelay(True)
        time_window.clear()
        time_window.addstr(format_seconds(timer.break_time_in_seconds)[0:],
                           curses.A_BOLD)
        time_window.refresh()
        try:
            timer_character = time_window.getkey()
            if timer_character == "p":
                timer.pause()
                
                info.update({"timer_state": States.PAUSE.value})
                info.update({"leftover_break_time_in_seconds": timer.break_time_in_seconds})
                with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                    dump(info, info_file, indent=2)
        except curses.error:
            timer_character = None
