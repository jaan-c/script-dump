from typing import *
import sys, os
from .. import delete_duplicates, keep


def interactive_delete(duplicate_groups: Mapping[str, Sequence[str]]) -> None:
    for hash, duplicates in duplicate_groups.items():
        print()
        print(hash)
        _print_with_position(duplicates)

        position = _prompt_position(len(duplicates))

        if position:
            delete_duplicates(
                keep.duplicate_position(position),
                duplicates,
                delete_file=_delete_with_logging,
            )
        else:
            print()
            print(f"skipped {hash}")


def _print_with_position(duplicates: Sequence[str]) -> None:
    position_width = 4
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