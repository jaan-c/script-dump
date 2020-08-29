from typing import *
from .duplicates import FileInfo


class Cli:
    duplicates: Mapping[str, List[FileInfo]]

    def __init__(self, duplicates: Mapping[str, List[FileInfo]]):
        self.duplicates = duplicates

    def run(self) -> None:
        raise NotImplementedError()


class InteractiveCli(Cli):
    def run(self) -> None:
        pass


class NonInteractiveCli(Cli):
    keep_most_recent: bool

    def __init__(
        self, duplicates: Mapping[str, List[FileInfo]], keep_most_recent: bool
    ):
        super(NonInteractiveCli, self).__init__(duplicates)
        self.keep_most_recent = keep_most_recent

    def run(self) -> None:
        pass
