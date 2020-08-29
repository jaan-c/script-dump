from typing import *
import itertools
from .files import FileInfo

K = TypeVar("K")
V = TypeVar("V")


def find_duplicates(
    file_infos: Iterable[FileInfo],
) -> Mapping[str, List[FileInfo]]:
    """ Find duplicates in infos and return it as a mapping of hash and file 
        paths. This skips over zero-byte files.
    """

    size_group = _group_by_key(file_infos, lambda i: i.get_size())
    size_group = {
        size: infos for size, infos in size_group.items() if size != 0
    }
    size_group = _remove_singleton_values(size_group)
    infos = _ungroup(size_group)

    partial_hash_group = _group_by_key(infos, lambda i: i.get_partial_hash())
    partial_hash_group = _remove_singleton_values(partial_hash_group)
    infos = _ungroup(partial_hash_group)

    hash_group = _group_by_key(infos, lambda i: i.get_hash())
    hash_group = _remove_singleton_values(hash_group)

    return hash_group


def _group_by_key(
    values: Iterable[V], derive_group_key: Callable[[V], K]
) -> Mapping[K, List[V]]:
    """ Group values by a key derived from each value. """

    group: Dict[K, List[V]] = {}
    for value in values:
        key = derive_group_key(value)
        if key in group:
            group[key].append(value)
        else:
            group[key] = [value]

    return group


def _ungroup(group: Mapping[K, Iterable[V]]) -> Iterable[V]:
    """ Remove grouping by merging all iterable values into one single iterable. 
    """

    return itertools.chain.from_iterable(group.values())


def _remove_singleton_values(
    mapping: Mapping[K, List[V]]
) -> Mapping[K, List[V]]:
    return {k: v for k, v in mapping.items() if len(v) != 1}
