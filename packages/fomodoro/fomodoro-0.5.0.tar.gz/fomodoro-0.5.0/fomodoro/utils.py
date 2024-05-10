"""
On this module there are util code.
"""
from enum import Enum
from os.path import dirname, abspath, join
from time import gmtime, strftime


TIME_FORMAT = '%H:%M:%S'

INFO_FILE = join(dirname(abspath(__file__)), 'info.json')

DATA_BASE_FILE = join(dirname(abspath(__file__)), 'fomodoro_terminal.db')

BELL_SOUND_FILE = join(dirname(abspath(__file__)), 'bell.wav')


class States(Enum):
    """
    States of the stopwatch and the timer.
    """
    WITHOUT_START: str = ' '
    START: str = 'Start'
    PAUSE: str = 'Pause'
    STOP: str = 'Stop'


def format_seconds(seconds: int) -> str:
    struct_time = gmtime(float(seconds))
    formated_seconds = strftime(TIME_FORMAT, struct_time)

    return formated_seconds
