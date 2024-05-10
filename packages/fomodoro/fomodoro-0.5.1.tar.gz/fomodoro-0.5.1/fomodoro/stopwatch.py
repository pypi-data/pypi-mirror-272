"""
This module has all code related to stopwatch.
"""
from json import load, dump
from time import sleep
import curses

from fomodoro.utils import States, INFO_FILE, format_seconds
from fomodoro.stats import add_stopwatch_record


class Stopwatch():
    """
    To can manipulate the stopwatch easiest by methods.
    """
    def __init__(self) -> None:
        self.state = States.WITHOUT_START
        self.elapsed_seconds: int = 0
        self.seconds: int = 0

    def start(self):
        self.state = States.START

    def pause(self):
        self.state = States.PAUSE

    def stop(self):
        self.state = States.STOP


stopwatch_obj = Stopwatch()


def prepare_stopwatch() -> Stopwatch:
    """
    This function will prepare the stopwatch obj to run stopwatch.
    """
    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        info: dict = load(info_file)

    stopwatch_obj.start()
    stopwatch_obj.elapsed_seconds = info["elapsed_seconds"]

    return stopwatch_obj


def run_stopwatch(stopwatch: Stopwatch):
    """
    This function run stopwatch.
    """
    time_window = curses.newwin(1, 9, 1, 16)

    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        info: dict = load(info_file)

    while stopwatch.state is States.START:
        sleep(1.0)
        stopwatch.elapsed_seconds += 1
        stopwatch.seconds += 1

        time_window.nodelay(True)
        time_window.clear()
        time_window.addstr(format_seconds(stopwatch.elapsed_seconds)[0:],
                           curses.A_BOLD)
        time_window.refresh()
        try:
            stopwatch_character = time_window.getkey()
            if stopwatch_character == "p":
                stopwatch.pause()
                info.update({"stopwatch_state": States.PAUSE.value})
                info.update({"elapsed_seconds": info["elapsed_seconds"] + stopwatch.seconds})
                with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                    dump(info, info_file, indent=2)
            elif stopwatch_character == "s":
                stopwatch.stop()
                info.update({"stopwatch_state": States.STOP.value})
                info.update({"elapsed_seconds": info["elapsed_seconds"] + stopwatch.seconds})
                add_stopwatch_record(info["elapsed_seconds"])
                with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                    dump(info, info_file, indent=2)
        except curses.error:
            stopwatch_character = None
