from typing import *
import pytest
import os, tempfile
from . import util
from .. import fileinfo

FILEINFO_FUNCS: Final = [
    fileinfo.get_size,
    fileinfo.get_modification_datetime,
    fileinfo.get_partial_hash,
    fileinfo.get_hash,
]


def test_fileinfo_funcs_with_non_existent_file():
    """fileinfo functions raises FileNotFoundError with non-existent files."""

    path = os.path.join(".", util.rand_file_name())
    for func in FILEINFO_FUNCS:
        with pytest.raises(FileNotFoundError):
            func(path)


def test_fileinfo_funcs_with_existing_file():
    """fileinfo functions returns anything except None with existing file."""

    for func in FILEINFO_FUNCS:
        with util.temp_file_with_rand_content(1024 * 10) as file_path:
            assert func(file_path) is not None
