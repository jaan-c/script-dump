from typing import *
import pytest
import string
from .context import FileInfo, list_descendant_files, InvalidPathException
from .utils import temp_file_of_size, temp_file_with_contents, get_random_bytes


class TestFileInfo:
    def test_get_size_with_empty_file(self):
        zero_size = 0
        with temp_file_of_size(zero_size) as path:
            assert FileInfo(path).get_size() == zero_size

    def test_get_size_with_non_empty_file(self):
        size = 1024
        with temp_file_of_size(size) as path:
            assert FileInfo(path).get_size() == size

    def test_hashes_are_hex_string(self):
        with temp_file_of_size(2048) as path:
            info = FileInfo(path)
            partial_hash = info.get_partial_hash()
            hash = info.get_hash()

            assert partial_hash
            assert hash

            assert is_hex_string(partial_hash)
            assert is_hex_string(hash)

    def test_partial_hash_with_same_file_head(self):
        head = get_random_bytes(1024)
        tail = get_random_bytes(1024)

        with temp_file_with_contents(head) as px, temp_file_with_contents(
            head + tail
        ) as py:
            assert (
                FileInfo(px).get_partial_hash()
                == FileInfo(py).get_partial_hash()
            )

    def test_partial_hash_with_different_file_head(self):
        head1 = get_random_bytes(1024)
        head2 = get_random_bytes(1024)
        tail = get_random_bytes(1024)

        with temp_file_with_contents(
            head1 + tail
        ) as px, temp_file_with_contents(head2 + tail) as py:
            assert (
                FileInfo(px).get_partial_hash()
                != FileInfo(py).get_partial_hash()
            )

    def test_hash_with_same_file_content(self):
        content = get_random_bytes(2048)

        with temp_file_with_contents(content) as px, temp_file_with_contents(
            content
        ) as py:
            assert FileInfo(px).get_hash() == FileInfo(py).get_hash()

    def test_hash_with_different_file_content(self):
        with temp_file_of_size(2048) as px, temp_file_of_size(2048) as py:
            assert FileInfo(px).get_hash() != FileInfo(py).get_hash()

    def test_get_partial_hash_and_get_hash_with_big_file(self):
        content = get_random_bytes(2048)

        with temp_file_with_contents(content) as path:
            info = FileInfo(path)
            assert info.get_partial_hash() != info.get_hash()


def test_list_descendant_files_with_file_path():
    with temp_file_of_size(0) as file_path:
        with pytest.raises(InvalidPathException):
            list_descendant_files(file_path)


def is_hex_string(text: str) -> bool:
    return all(c in string.hexdigits for c in text)

