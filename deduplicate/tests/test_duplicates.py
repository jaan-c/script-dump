from typing import *
import pytest
from tempfile import TemporaryDirectory
from .context import find_duplicates, FileInfo
from .utils import temp_file_with_contents, temp_file_of_size, get_random_bytes


def test_find_duplicates():
    with TemporaryDirectory() as dir:
        head1, head2, head3, tail = (get_random_bytes(2048) for _ in range(4))

        with temp_file_with_contents(
            head1 + tail
        ) as ph1, temp_file_with_contents(
            head2 + tail
        ) as ph2, temp_file_with_contents(
            head3 + tail
        ) as h1, temp_file_with_contents(
            head3 + tail
        ) as h2, temp_file_of_size(
            2048
        ) as r1, temp_file_of_size(
            2048
        ) as r2:
            # ph1, ph2: partial hash matches
            # h1, h2: full hash matches
            # r1, r2: completely random content but same size
            infos = map(FileInfo, [ph1, ph2, h1, h2, r1, r2])
            duplicates = find_duplicates(infos)

            assert len(duplicates.keys()) == 1
            assert sum(len(infos) for infos in duplicates.values()) == 2
            assert set(
                map(lambda i: i.path, duplicates[FileInfo(h1).get_hash()])
            ) == {h1, h2}

