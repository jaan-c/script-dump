from typing import *
from typing import IO
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory
from random import getrandbits
import os


@contextmanager
def temp_file_of_size(size: int, dir: Optional[str] = None) -> Iterator[str]:
    """ Create temporary file of specified size, filled with random data and 
        yield the absolute path. The path will be removed on context exit.
    """

    with NamedTemporaryFile(mode="wb", delete=False, dir=dir) as file:
        content = get_random_bytes(size)
        file.write(content)
        path = file.name

    try:
        yield path
    finally:
        os.remove(path)


@contextmanager
def temp_file_with_contents(
    content: bytearray, dir: Optional[str] = None
) -> Iterator[str]:
    """ Create temporary file containing content and yield the absolute path.
        The path will be removed on context exit.
    """

    with NamedTemporaryFile(mode="wb", delete=False, dir=dir) as file:
        file.write(content)
        path = file.name

    try:
        yield path
    finally:
        os.remove(path)


def get_random_bytes(count: int) -> bytearray:
    return bytearray(getrandbits(8) for _ in range(count))
