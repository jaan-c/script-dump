from typing import *
import pytest
from .. import find, fileinfo
from . import util
import tempfile


def test_find_duplicates():
    head1, head2, head3, body = (util.rand_bytes(1024) for _ in range(4))

    with tempfile.TemporaryDirectory() as dir_path:
        with util.temp_file_with_rand_content(
            0, dir_path
        ) as z1, util.temp_file_with_rand_content(
            0, dir_path
        ) as z2, util.temp_file_with_content(
            head1 + body, dir_path
        ) as ph1, util.temp_file_with_content(
            head2 + body, dir_path
        ) as ph2, util.temp_file_with_content(
            head3 + body, dir_path
        ) as h1, util.temp_file_with_content(
            head3 + body, dir_path
        ) as h2, util.temp_file_with_rand_content(
            2048, dir_path
        ) as r1, util.temp_file_with_rand_content(
            2048, dir_path
        ) as r2:
            duplicate_groups = find.find_duplicates(dir_path)

            assert len(duplicate_groups) == 1
            assert duplicate_groups == {fileinfo.get_hash(h1): [h1, h2]}
