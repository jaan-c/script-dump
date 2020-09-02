from typing import *
import functools
from . import delete
from . import fileinfo


def _return_keep_filter(keep_filter: delete.KeepFilter):
    """Wrap keep_filter inside an empty argument function that returns it."""

    @functools.wraps(keep_filter)
    def return_keep_filter() -> delete.KeepFilter:
        nonlocal keep_filter
        return keep_filter

    return return_keep_filter


def duplicate_position(position: int) -> delete.KeepFilter:
    def keep_duplicate_position(
        duplicate_paths: Sequence[str],
    ) -> Sequence[str]:
        nonlocal position

        if not (1 <= position <= len(duplicate_paths)):
            raise delete.StateError("position out of range")

        return [duplicate_paths[position - 1]]

    return keep_duplicate_position


@_return_keep_filter
def last_modified(duplicate_paths: Sequence[str]) -> Sequence[str]:
    mod_datetimes = map(fileinfo.get_modification_datetime, duplicate_paths)
    most_recent_datetime_ix = list(mod_datetimes).index(max(mod_datetimes))

    return [duplicate_paths[most_recent_datetime_ix]]
