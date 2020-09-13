from typing import *
import os, re


class FileTag:
    path: str
    tags: Sequence[str]

    def __init__(self, path: str, tags: Sequence[str]):
        self.path = os.path.abspath(path)
        self.tags = [self._normalize_tag(t) for t in tags]

    def _normalize_tag(self, tag: str) -> str:
        tag = tag.strip().lower()

        valid_tag = r"^[a-z0-9][a-z0-9-_.]+$"
        if not re.match(valid_tag, tag):
            raise ValueError(f"invalid tag '{tag}'")

        return tag