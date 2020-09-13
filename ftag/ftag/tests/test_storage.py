from typing import *
import pytest
import tempfile
from .. import logic, storage


def test_save_is_inverse_of_read():
    file_tags = [
        logic.FileTag("/home/mitlof/mitlof_file", ["mitlof"]),
        logic.FileTag("/home/mitlof/biflof_file", ["mitlof", "biflof"]),
    ]

    with tempfile.NamedTemporaryFile() as file:
        storage.save_file_tags(file_tags, path=file.name)
        assert storage.read_file_tags(path=file.name) == file_tags