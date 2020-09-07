from typing import *
import random, string, datetime, contextlib, tempfile, os


def rand_file_name(length: int = 16) -> str:
    valid_chars = string.ascii_lowercase + string.digits + "-_."
    return "".join(random.choices(valid_chars, k=length))


def rand_bytes(size: int) -> bytes:
    return bytes(random.getrandbits(8) for _ in range(size))


@contextlib.contextmanager
def temp_file_with_mtime(
    modification_datetime: datetime.datetime,
) -> Iterator[str]:
    try:
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file_path = file.name
            atime = os.path.getatime(file_path)
            os.utime(file_path, (atime, modification_datetime.timestamp()))

        yield file_path
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.remove(file_path)


@contextlib.contextmanager
def temp_file_with_content(content: bytes) -> Iterator[str]:
    try:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as file:
            file_path = file.name
            file.write(content)

        yield file_path
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.remove(file_path)
