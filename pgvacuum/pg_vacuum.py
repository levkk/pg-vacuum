#
# Manage PostgreSQL vacuum madness.
#

import psycopg2
from psycopg2.extras import DictCursor

import colorama
from colorama import Fore, Style
import click
from prettytable import PrettyTable  # Pretty table output

import os

VERSION = "0.1-alpha4"

__author__ = "lev.kokotov@instacart.com"
__version__ = VERSION

colorama.init()


def _error2(text):
    print(Fore.RED, "\b{}".format(text), Fore.RESET)
    if os.getenv("EXIT_ON_ERROR"):
        exit(1)


def _result2(text):
    print(Fore.GREEN, "\b{}".format(text), Fore.RESET)


def _debug(cursor):
    """Print the executed query in a pretty color."""
    if os.getenv("DEBUG"):
        print(
            Fore.BLUE,
            "\b{}: ".format(cursor.connection.dsn) + cursor.query.decode("utf-8"),
            Fore.RESET,
        )


def _exec(cursor, query, params=None):
    """Execute the query with params"""
    cursor.execute(query, params)
    _debug(cursor)
    return cursor


# Credit: https://gist.github.com/thatalextaylor/7408395
def _pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return "%dd%dh%dm%ds" % (days, hours, minutes, seconds)
    elif hours > 0:
        return "%dh%dm%ds" % (hours, minutes, seconds)
    elif minutes > 0:
        return "%dm%ds" % (minutes, seconds)
    else:
        return "%ds" % (seconds,)


def _table(headers, rows):
    """Build a nice table with headers."""
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
    return table


def show_progress(conn):
    query = """
    SELECT
        pg_stat_progress_vacuum.pid AS pid,
        relname,
        phase,
        (heap_blks_scanned / heap_blks_total * 100) AS heap_progress,
        query_start,
        (NOW() - query_start) AS duration
    FROM pg_stat_progress_vacuum
    INNER JOIN pg_class
        ON pg_class.oid = pg_stat_progress_vacuum.datid
    INNER JOIN pg_stat_activity
        ON pg_stat_activity.pid = pg_stat_progress_vacuum.pid
    """
    rows = _exec(conn, query, query).fetchall()
    if not rows:
        _result2("No vacuums/autovacuums running.")
    else:
        _result2(
            _table(["PID", "Table", "Phase", "Progress", "Started", "Duration"], rows)
        )


def show_vacuum(conn):
    query = """
    SELECT
        pid,
        query,
        query_start,
        NOW() - query_start AS duration
    FROM pg_stat_activity
    WHERE query LIKE 'autovacuum:%' OR query ILIKE 'VACUUM%'
    AND state != 'idle'
    """
    rows = _exec(conn, query).fetchall()
    if not rows:
        _result2("No vacuums/autovacuums running.")
    else:
        _result2(_table(["PID", "Query", "Started", "Duration"], rows))


def kill_autovacuum(conn, pid):
    """Kill a running autovacuum/vacuum process.
    
    Parameters:
        - conn: psycopg2.Cursor
        - pid: process ID
    """
    assert pid is not None
    # This will terminate the PID only if it's a vacuum/autovacuum.
    query = """
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE (
        query LIKE 'autovacuum:%%'
        OR
        query ILIKE 'VACUUM%%'
    ) AND pid = %s
    """
    done = _exec(conn, query, (pid,)).fetchone()

    if done is None:
        _error2("No vacuum/autovacuum with PID={} running.".format(pid))
    else:
        _result2("OK.")


def show_table_options(conn, table):
    query = """
    SELECT relname, reloptions FROM pg_class WHERE relname = %s;
    """
    settings = _exec(conn, query, (table,)).fetchone()
    if not settings:
        _error2('Table "{}" does not exist.'.format(table))
    else:
        opts = settings["reloptions"]
        _result2(_table(["Setting", "Value"], map(lambda x: x.split("="), opts)))


def table_autovacuum(conn, table, enable):
    """Enable or disable autovacuum on a particular table."""
    query = """
    BEGIN;
    SET lock_timeout = '1s';
    ALTER TABLE {} SET (autovacuum_enabled = {}, toast.autovacuum_enabled = {});
    COMMIT;
    """
    enable = "true" if enable else "false"
    _exec(conn, query.format(table, enable, enable))
    if enable == "true":
        _result2('Autovacuum enabled on table "{}".'.format(table))
    if enable == "false":
        _result2('Autovacuum disabled on table "{}".'.format(table))


@click.command()
@click.option(
    "--database", required=True, help="DSN/URL of the database to connect to."
)
@click.option("--kill", required=False, help="PID of the vacuum process to terminate.")
@click.option(
    "--progress/--no-progress",
    required=False,
    help="Show progress of autovacuums/vacuums running.",
)
@click.option(
    "--debug/--no-debug", required=False, help="Print SQL statements that were ran."
)
@click.option(
    "--table", required=False, help="Enable/disable autovacuum on that table."
)
@click.option(
    "--enable/--disable",
    required=False,
    default=None,
    help="Enable/disable autovacuum.",
)
def cli(database, kill, progress, debug, table, enable):
    conn = psycopg2.connect(database, connect_timeout=5)
    cursor = conn.cursor(cursor_factory=DictCursor)

    try:
        if debug:
            os.environ["DEBUG"] = "True"
        if kill:
            kill_autovacuum(cursor, kill)
        elif progress:
            show_progress(cursor)
        elif table is not None and enable is None:
            show_table_options(cursor, table)
        elif table and enable is not None:
            table_autovacuum(cursor, table, enable)
        else:
            show_vacuum(cursor)
    finally:
        conn.commit()
        conn.close()
