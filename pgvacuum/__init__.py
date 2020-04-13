from .pg_vacuum import VERSION
from .pg_vacuum import cli


def main():
    cli(prog_name="pgvacuum")
