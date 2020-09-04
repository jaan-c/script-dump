from typing import *
import argparse
from . import duplicate, delete, keep


def execute(raw_cli_args: Sequence[str]) -> None:
    cli_args = _parse_args(raw_cli_args)

    print("Finding duplicates.")
    duplicate_groups = duplicate.find_duplicates(cli_args.dir_path)

    exit()
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
    parser.add_argument("dir", type=str, help="directory to deduplicate")
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
        keep_filter="last_modified" if parsed.keep_filter else None,
    )


def _interactive_delete(duplicate_groups: Mapping[str, Sequence[str]]) -> None:
    pass
