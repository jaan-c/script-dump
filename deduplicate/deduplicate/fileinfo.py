from typing import *
import os, datetime, hashlib


def get_size(file_path: str) -> int:
    return os.path.getsize(file_path)


def get_modification_datetime(file_path: str) -> datetime.datetime:
    seconds_since_epoch = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(seconds_since_epoch)


def get_head_hash(file_path: str, size: int = 1024) -> str:
    with open(file_path, "rb") as file:
        head = file.read(1024)
        return hashlib.sha256(head).hexdigest()


def get_hash(file_path: str, chunk_size: int = 8388608) -> str:
    with open(file_path, "rb") as file:
        hash_sink = hashlib.sha256()
        while chunk := file.read(chunk_size):
            hash_sink.update(chunk)

        return hash_sink.hexdigest()
