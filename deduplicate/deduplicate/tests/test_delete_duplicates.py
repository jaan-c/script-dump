from typing import *
import pytest
from .. import KeepFilter, delete_duplicates
from ..delete import KeepFilterError
from . import util
import os


def test_delete_duplicates_with_empty_keep_filter():
    empty_keep_filter: KeepFilter = lambda _: []
    file_size = 1024 * 10

    with util.temp_file_with_rand_content(
        file_size
    ) as p1, util.temp_file_with_rand_content(
        file_size
    ) as p2, util.temp_file_with_rand_content(
        file_size
    ) as p3:
        duplicates = [p1, p2, p3]
        delete_duplicates(empty_keep_filter, duplicates)

        for p in duplicates:
            assert not os.path.exists(p)


def test_delete_duplicates_with_id_keep_filter():
    id_keep_filter: KeepFilter = lambda duplicates: duplicates
    file_size = 1024 * 10

    with util.temp_file_with_rand_content(
        file_size
    ) as p1, util.temp_file_with_rand_content(
        file_size
    ) as p2, util.temp_file_with_rand_content(
        file_size
    ) as p3:
        duplicates = [p1, p2, p3]
        delete_duplicates(id_keep_filter, duplicates)

        for p in duplicates:
            assert os.path.exists(p)


def test_delete_duplicates_with_malformed_keep_filter():
    """Test delete_duplicates against a KeepFilter yielding a non-subset of
    passed duplicate_paths."""

    duplicates = [util.rand_file_name() for _ in range(5)]
    malformed_keep_filter: KeepFilter = lambda duplicates: [
        duplicates[0],
        "not in duplicates",
    ]

    with pytest.raises(KeepFilterError):
        delete_duplicates(malformed_keep_filter, duplicates)
