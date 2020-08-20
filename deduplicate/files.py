from typing import *
import os
import hashlib


class FileInfo:
    path: str
    _size: Optional[int]
    _partial_hash: Optional[str]
    _hash: Optional[str]

    def __init__(self, path: str):
        self.path = path
        self._size = None
        self._partial_hash = None
        self._hash = None

    def get_size(self) -> int:
        if self._size == None:
            self._size = os.path.getsize(self.path)

        assert isinstance(self._size, int)
        return self._size

    def get_partial_hash(self) -> str:
        if self._partial_hash == None:
            self._partial_hash = _Hash.partial(self.path)

        assert isinstance(self._partial_hash, str)
        return self._partial_hash

    def get_hash(self) -> str:
        if self._hash == None:
            self._hash = _Hash.full(self.path)

        assert isinstance(self._hash, str)
        return self._hash

    def __repr__(self) -> str:
        return f"FileInfo(path={self.path}, size={self.get_size()}, partial_hash={self.get_partial_hash()}, hash={self.get_hash()})"


class _Hash:
    @staticmethod
    def partial(file_path: str, size: int = 1024) -> str:
        """ Compute checksum of file_path for the first size bytes of file. """

        with open(file_path, "rb") as file:
            byte = file.read(size)
            sha256 = hashlib.sha256(byte).hexdigest()
            return sha256

    @staticmethod
    def full(file_path: str, chunk_size=8388608) -> str:
        """ Compute checksum for file_path. chunk_size defaults to 8 MB."""

        with open(file_path, "rb") as file:
            hash_sink = hashlib.sha256()
            chunk = file.read(chunk_size)
            while chunk:
                hash_sink.update(chunk)
                chunk = file.read(chunk_size)

            return hash_sink.hexdigest()


def list_descendant_files(root_dir_path: str) -> Iterable[FileInfo]:
    """ Generates absolute paths of descendant files in root_dir_path. """

    for dir_path, _, file_names in os.walk(root_dir_path):
        dir_path = os.path.abspath(dir_path)
        file_paths = map(lambda name: os.path.join(dir_path, name), file_names)
        for p in file_paths:
            yield FileInfo(p)
