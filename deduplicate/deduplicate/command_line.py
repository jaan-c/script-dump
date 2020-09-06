from typing import *
import sys, os, argparse
from . import duplicate, delete, keep


def main() -> None:
    cli_args = _parse_args(sys.argv[1:])

    print("Finding duplicates.")
    duplicate_groups = duplicate.find_duplicates(cli_args.dir_path)

    if not cli_args.keep_filter:
        _interactive_delete(duplicate_groups)
    else:
        # Guard against newly added keep filters.
        assert cli_args.keep_filter == "last_modified"

        for duplicates in duplicate_groups.values():
            delete.delete_duplicates(keep.last_modified(), duplicates)


class _CliArgs(NamedTuple):
    dir_path: str
    keep_filter: Optional[Literal["last_modified"]]


def _parse_args(raw_cli_args: Sequence[str]) -> _CliArgs:
    parser = argparse.ArgumentParser(
        description="recursively deduplicate files in dir_path",
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

    parsed = parser.parse_args(raw_cli_args)
    return _CliArgs(
        dir_path=parsed.dir,
        keep_filter="last_modified"
        if parsed.keep_filter == "last-modified"
        else None,
    )


def _interactive_delete(duplicate_groups: Mapping[str, Sequence[str]]) -> None:
    for hash, duplicates in duplicate_groups.items():
        print()
        print(hash)
        _print_with_position(duplicates)

        position = _prompt_position(len(duplicates))

        if position:
            delete.delete_duplicates(
                keep.duplicate_position(position),
                duplicates,
                delete_file=_delete_with_logging,
            )
        else:
            print(f"skipped {hash}")


def _print_with_position(duplicates: Sequence[str]) -> None:
    position_width = 3
    for position, path in zip(range(1, len(duplicates) + 1), duplicates):
        print(f"{str(position).rjust(position_width)}.) {path}")


def _prompt_position(length: int) -> Optional[int]:
    while True:
        try:
            raw_position = input("# of path to keep or 'skip'> ")
        except KeyboardInterrupt:
            sys.exit(0)

        try:
            if raw_position.strip().lower() in ("s", "skip"):
                return None
            else:
                position = int(raw_position)
                if 1 <= position <= length:
                    return position
        except ValueError:
            continue


def _delete_with_logging(file_path: str) -> None:
    os.remove(file_path)
    print(f"deleted {file_path}")