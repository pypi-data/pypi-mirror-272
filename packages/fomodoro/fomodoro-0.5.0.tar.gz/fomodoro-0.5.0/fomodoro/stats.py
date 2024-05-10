"""
This module has all code related to stats feature.
"""
from datetime import datetime
from sqlite3 import connect, OperationalError, Cursor, Connection
import click as ck
from rich.table import Table
from rich.console import Console

from fomodoro.utils import DATA_BASE_FILE, format_seconds


# IDEA FOR TEST: Print whatever raised exception on code that use sqlite3.
def create_table(cursor: Cursor,
                 connection: Connection,
                 table_name: str) -> None:
    """
    This function create stopwatch and timer tables
    on fomodoro_terminal database.
    """
    try:
        cursor.execute(
            f"""
            CREATE TABLE {table_name}(
            id INTEGER NOT NULL,
            seconds INTEGER NOT NULL,
            date TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT)
            );
            """
        )
        connection.commit()
    except OperationalError:
        pass


def add_stopwatch_record(elapsed_seconds: int) -> None:
    """
    This function create a new record on stopwatch table.
    """
    date = datetime.now().isoformat()[0:10]
    week = datetime.now().strftime('%W')

    connection = connect(DATA_BASE_FILE)
    cursor = connection.cursor()

    create_table(cursor, connection, "stopwatch")

    # IDEA FOR TEST: After execute this function execute a select query
    # to compare result data with insert insert data.
    cursor.execute(
        """
        INSERT INTO stopwatch(seconds, date) VALUES (?, ?)
        """,
        (elapsed_seconds, f"{date},{week}")
    )
    connection.commit()

    connection.close()


def add_timer_record(amount_of_seconds_for_the_timer: int) -> None:
    """
    This function create a new record on timer table.
    """
    date = datetime.now().isoformat()[0:10]
    week = datetime.now().strftime('%W')

    connection = connect(DATA_BASE_FILE)
    cursor = connection.cursor()

    create_table(cursor, connection, "timer")

    # IDEA FOR TEST: After execute this function execute a select query
    # to compare result data with insert insert data.
    cursor.execute(
        """
        INSERT INTO timer(seconds, date) VALUES (?, ?)
        """,
        (amount_of_seconds_for_the_timer, f"{date},{week}")
    )
    connection.commit()

    connection.close()


def get_seconds() -> list[tuple[tuple, tuple, tuple, tuple]]:
    """
    This function get stopwatch and timer seconds
    associated with whatever day, week, month, year.
    """
    day = datetime.now().strftime('%d')
    week = datetime.now().strftime('%W')
    month = datetime.now().strftime('%m')
    year = datetime.now().strftime('%Y')

    connection = connect(DATA_BASE_FILE)
    cursor = connection.cursor()

    sum_of_the_stopwatch_seconds_associated_with_day = cursor.execute(
        f"""
        SELECT sum(seconds) FROM stopwatch
        WHERE date LIKE '{year}-{month}-{day},%'
        """
    ).fetchone()
    sum_of_the_stopwatch_seconds_associated_with_week = cursor.execute(
        f"""
        SELECT sum(seconds) FROM stopwatch
        WHERE date LIKE '{year}%,{week}'
        """
    ).fetchone()
    sum_of_the_stopwatch_seconds_associated_with_month = cursor.execute(
        f"""
        SELECT sum(seconds) FROM stopwatch
        WHERE date LIKE '{year}-{month}-__%'
        """
    ).fetchone()
    sum_of_the_stopwatch_seconds_associated_with_year = cursor.execute(
        f"""
        SELECT sum(seconds) FROM stopwatch
        WHERE date LIKE '{year}%'
        """
    ).fetchone()

    sum_of_the_timer_seconds_associated_with_day = cursor.execute(
        f"""
        SELECT sum(seconds) FROM timer
        WHERE date LIKE '{year}-{month}-{day},%'
        """
    ).fetchone()
    sum_of_the_timer_seconds_associated_with_week = cursor.execute(
        f"""
        SELECT sum(seconds) FROM timer
        WHERE date LIKE '{year}%,{week}'
        """
    ).fetchone()
    sum_of_the_timer_seconds_associated_with_month = cursor.execute(
        f"""
        SELECT sum(seconds) FROM timer
        WHERE date LIKE '{year}-{month}-__%'
        """
    ).fetchone()
    sum_of_the_timer_seconds_associated_with_year = cursor.execute(
        f"""
        SELECT sum(seconds) FROM timer
        WHERE date LIKE '{year}%'
        """
    ).fetchone()
    connection.close()

    return [
        (sum_of_the_stopwatch_seconds_associated_with_day,
         sum_of_the_stopwatch_seconds_associated_with_week,
         sum_of_the_stopwatch_seconds_associated_with_month,
         sum_of_the_stopwatch_seconds_associated_with_year),
        (sum_of_the_timer_seconds_associated_with_day,
         sum_of_the_timer_seconds_associated_with_week,
         sum_of_the_timer_seconds_associated_with_month,
         sum_of_the_timer_seconds_associated_with_year)
        ]


@ck.command
def show_stats():
    """
    This command shows stopwatch and timer stats to the user.
    """
    time_periods = ("Daily", "Week", "Monthly", "Yearly")
    sum_of_seconds = get_seconds()
    stopwatch_seconds = sum_of_seconds[0]
    timer_seconds = sum_of_seconds[1]

    stats_table = Table("", "Work/Study", "Break",
                        title="Stats", title_justify="center",
                        show_lines=True, title_style="bold italic")

    for time_period, work_study_seconds, break_seconds in zip(time_periods, stopwatch_seconds, timer_seconds):
        work_study_seconds_formatted = format_seconds(work_study_seconds[0])
        break_seconds_formatted = format_seconds(break_seconds[0])

        stats_table.add_row(time_period, work_study_seconds_formatted, break_seconds_formatted)

    console = Console()
    console.print(stats_table)
