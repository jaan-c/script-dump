from typing import *
import argparse, sys


class CommandLineArgs(NamedTuple):
    dir_path: str
    show_only: bool
    keep_filter: Optional[Literal["last_modified"]]


def parse_args(raw_cli_args: Sequence[str] = sys.argv) -> CommandLineArgs:
    parser = argparse.ArgumentParser(
        description="""
            recursively delete duplicate files in a directory
        """,
        epilog="""
            If no --keep-filter is supplied, deduplication happens 
            interactively.
        """,
    )
    parser.add_argument("dir", help="directory to deduplicate")
    parser.add_argument(
        "--show-only",
        help="only display duplicates, no deletion happens",
        action="store_true",
    )
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
        show_only=parsed.show_only,
        keep_filter="last_modified"
        if parsed.keep_filter == "last-modified"
        else None,
    )