from typing import *
import random, string, datetime, contextlib, tempfile, os


def rand_file_name(length: int = 16) -> str:
    valid_chars = string.ascii_lowercase + string.digits + "-_."
    return "".join(random.choices(valid_chars, k=length))


def rand_bytes(size: int) -> bytes:
    return bytes(random.getrandbits(8) for _ in range(size))


@contextlib.contextmanager
def temp_file_with_mtime(
    modification_datetime: datetime.datetime, dir_path: Optional[str] = None
) -> Iterator[str]:
    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=dir_path) as file:
            file_path = file.name
            atime = os.path.getatime(file_path)
            os.utime(file_path, (atime, modification_datetime.timestamp()))

        yield file_path
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.remove(file_path)


@contextlib.contextmanager
def temp_file_with_content(
    content: bytes, dir_path: Optional[str] = None
) -> Iterator[str]:
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, dir=dir_path
        ) as file:
            file_path = file.name
            file.write(content)

        yield file_path
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.remove(file_path)


@contextlib.contextmanager
def temp_file_with_rand_content(
    size: int, dir_path: Optional[str] = None
) -> Iterator[str]:
    with temp_file_with_content(rand_bytes(size), dir_path) as file_path:
        yield file_path