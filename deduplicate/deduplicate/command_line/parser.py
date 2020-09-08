from typing import *
import argparse, sys


class CommandLineArgs(NamedTuple):
    dir_path: str
    keep_filter: Optional[Literal["last_modified"]]


def parse_args(raw_cli_args: Sequence[str] = sys.argv) -> CommandLineArgs:
    parser = argparse.ArgumentParser(
        description="""
            recursively delete duplicate files in a directory interactively
            or automatically with a keep filter
        """,
        epilog="""
            If --keep-filter is supplied, deduplication happens automatically, 
            otherwise an interactive interface is shown.
        """,
    )
    parser.add_argument("dir", help="directory to deduplicate")
    parser.add_argument(
        "--keep-filter",
        choices=["last-modified"],
        help="""
            automatic deduplication with supplied keep filter, passing 
            'last_modified' keeps the most recently modified file and deletes 
            everything else
        """,
    )

    parsed = parser.parse_args(raw_cli_args[1:])
    return CommandLineArgs(
        dir_path=parsed.dir,
        keep_filter="last_modified"
        if parsed.keep_filter == "last-modified"
        else None,
    )