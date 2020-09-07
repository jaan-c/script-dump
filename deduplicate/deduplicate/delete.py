from typing import *
import os


class KeepFilterError(Exception):
    pass


KeepFilter = Callable[[Sequence[str]], Sequence[str]]


def delete_duplicates(
    keep_filter: KeepFilter,
    duplicate_paths: Sequence[str],
    delete_file: Callable[[str], None] = os.remove,
) -> None:
    keep_paths = set(keep_filter(duplicate_paths))
    if not keep_paths.issubset(duplicate_paths):
        raise KeepFilterError(
            "keep_filter must return a subset of duplicate_paths"
        )

    for p in duplicate_paths:
        if p not in keep_paths:
            delete_file(p)
