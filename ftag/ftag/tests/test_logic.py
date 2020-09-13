from typing import *
import pytest
import os
from .. import logic


def test_file_tag_with_valid_input():
    path = "/home/mitlof/mitlof_file"
    tags = ["mitlof-_.", "biflof"]
    file_tag = logic.FileTag(path, tags)

    assert file_tag.path == path
    assert file_tag.tags == tags


def test_file_tag_with_relative_path():
    relative_path = "./mitlof_file"
    tags = ["mitlof", "biflof"]
    file_tag = logic.FileTag(relative_path, tags)

    assert file_tag.path == os.path.abspath(relative_path)


def test_file_tag_with_invalid_tag():
    path = "/home/mitlof/mitlof_file"

    with pytest.raises(ValueError):
        assert logic.FileTag(path, ["is_valid-tag1", "-invalid"])
