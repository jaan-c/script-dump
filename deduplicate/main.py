from typing import *
from argparse import ArgumentParser
from files import list_descendant_files, FileInfo
from duplicates import find_duplicates
from cli import InteractiveCli, NonInteractiveCli


CliArgs = NamedTuple("CliArgs", [("dir_path", str), ("keep_most_recent", bool)])


def parse_args() -> CliArgs:
    parser = ArgumentParser(
        description="recursively deduplicate files in dir_path",
        epilog="""
            If --keep-most-recent is supplied, deduplication happens 
            automatically, otherwise an interactive interface is shown.
        """,
    )
    parser.add_argument("dir_path", type=str, help="directory to deduplicate")
    parser.add_argument(
        "--keep-most-recent",
        action="store_true",
        help="automatically keep most recent file and delete other duplicates",
    )

    args = parser.parse_args()
    return CliArgs(
        dir_path=args.dir_path, keep_most_recent=args.keep_most_recent
    )


if __name__ == "__main__":
    args = parse_args()

    print("Building file list.")
    infos = list_descendant_files(args.dir_path)

    print("Finding duplicates.")
    duplicates = find_duplicates(infos)

    if args.keep_most_recent:
        NonInteractiveCli(duplicates, keep_most_recent=True).run()
    else:
        InteractiveCli(duplicates)
