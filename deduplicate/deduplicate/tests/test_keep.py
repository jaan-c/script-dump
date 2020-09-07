from typing import *
import pytest
import datetime
from . import util
from .. import keep, delete


def test_duplicate_position():
    duplicates = [util.rand_file_name() for _ in range(10)]

    assert keep.duplicate_position(3)(duplicates) == [duplicates[2]]

    with pytest.raises(delete.KeepFilterException):
        keep.duplicate_position(0)(duplicates)

    with pytest.raises(delete.KeepFilterException):
        keep.duplicate_position(11)(duplicates)


def test_last_modified():
    with util.temp_file_path_with_mtime(
        datetime.datetime.fromtimestamp(0)
    ) as p1, util.temp_file_path_with_mtime(
        datetime.datetime.now()
    ) as p2, util.temp_file_path_with_mtime(
        datetime.datetime(2000, 1, 1)
    ) as p3:
        assert keep.last_modified()([p1, p2, p3]) == [p2]