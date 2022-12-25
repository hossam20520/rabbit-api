# This file is only intended to serve global variables at a project-wide level.


def init_globals():
    from rich.console import Console

    global rc
    rc = Console(highlight=False) # Rich Console