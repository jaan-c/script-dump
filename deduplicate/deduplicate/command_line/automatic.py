from typing import *
from .. import delete_duplicates, keep


def automatic_delete(
    duplicate_groups: Mapping[str, Sequence[str]],
    keep_filter: Literal["last_modified"],
):
    for duplicates in duplicate_groups.values():
        delete_duplicates(keep.last_modified(), duplicates)
