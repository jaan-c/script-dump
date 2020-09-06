from typing import *
import itertools, functools, os
from . import fileinfo

K = TypeVar("K", bound=Hashable)


def find_duplicates(dir_path: str) -> Dict[str, List[str]]:
    """Find duplicate files in dir_path and return it as a mapping of hash
    to file paths. Zero-byte files are ignored."""

    file_paths = _walk_files(dir_path)

    grouped_by_size = _group_by(fileinfo.get_size, file_paths)
    grouped_by_size.pop(0, None)
    grouped_by_size = _omit_singleton_paths(grouped_by_size)
    file_paths = _ungroup(grouped_by_size)

    grouped_by_partial_hash = _group_by(fileinfo.get_partial_hash, file_paths)
    grouped_by_partial_hash = _omit_singleton_paths(grouped_by_partial_hash)
    file_paths = _ungroup(grouped_by_partial_hash)

    grouped_by_hash = _group_by(fileinfo.get_hash, file_paths)
    grouped_by_hash = _omit_singleton_paths(grouped_by_hash)

    return grouped_by_hash


def _walk_files(dir_path: str) -> Iterable[str]:
    for dir_path, _, file_names in os.walk(dir_path):
        file_paths = map(functools.partial(os.path.join, dir_path), file_names)
        yield from file_paths


def _group_by(
    derive_key: Callable[[str], K], paths: Iterable[str]
) -> Dict[K, List[str]]:
    path_groups: Dict[K, List[str]] = {}
    for p in paths:
        key = derive_key(p)
        if key in path_groups:
            path_groups[key].append(p)
        else:
            path_groups[key] = [p]

    return path_groups


def _ungroup(path_groups: Mapping[K, Sequence[str]]) -> Iterable[str]:
    return itertools.chain.from_iterable(path_groups.values())


def _omit_singleton_paths(
    path_groups: Dict[K, List[str]]
) -> Dict[K, List[str]]:
    return {key: paths for key, paths in path_groups.items() if len(paths) != 1}
