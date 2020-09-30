from typing import *


def show(duplicate_groups: Mapping[str, Sequence[str]]) -> None:
    for hash, duplicates in duplicate_groups.items():
        print(hash)
        for path in duplicates:
            print("\t" + path)