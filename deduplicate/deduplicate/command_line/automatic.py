from typing import *
import os
from .. import delete_duplicates, keep


def automatic_delete(
    duplicate_groups: Mapping[str, Sequence[str]],
    keep_filter: Literal["last_modified"],
):
    for duplicates in duplicate_groups.values():
        delete_duplicates(
            keep.last_modified(), duplicates, delete_file=_delete_with_logging
        )


def _delete_with_logging(file_path: str) -> None:
    os.remove(file_path)
    print(f"deleted {file_path}")