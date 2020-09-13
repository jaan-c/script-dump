from typing import *
import pytest
import tempfile
from .. import FileTag, save_file_tags, read_file_tags


def test_save_is_inverse_of_read():
    file_tags = [
        FileTag("/home/mitlof/mitlof_file", ["mitlof"]),
        FileTag("/home/mitlof/biflof_file", ["mitlof", "biflof"]),
    ]

    with tempfile.NamedTemporaryFile() as file:
        save_file_tags(file_tags, path=file.name)
        assert read_file_tags(path=file.name) == file_tags