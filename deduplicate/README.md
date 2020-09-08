# deduplicate

Recursively delete duplicate files in a directory interactively or
automatically with a keep filter.

## Installation

```
cd script-dump; pip3 install deduplicate/
```

The trailing slash is required, it tells pip3 to install a local package instead of a package in PyPi named deduplicate.

## As a Command

```
usage: deduplicate [-h] [--keep-filter {last-modified}] dir

recursively delete duplicate files in a directory interactively or
automatically with a keep filter

positional arguments:
  dir                   directory to deduplicate

optional arguments:
  -h, --help            show this help message and exit
  --keep-filter {last-modified}
                        automatic deduplication with supplied keep filter,
                        passing 'last_modified' keeps the most recently
                        modified file and deletes everything else

If --keep-filter is supplied, deduplication happens automatically, otherwise
an interactive interface is shown.
```

## As a Module

```
deduplicate
    find_duplicates(dir_path: str) -> Dict[str, List[str]]
    KeepFilter = Callable[[Sequence[str]], Sequence[str]]
    delete_duplicates(
        keep_filter: KeepFilter,
        duplicate_paths: Sequence[str],
        delete_file: Callable[[str], None] = os.remove
    )
    keep
        duplicate_position(position: int) -> KeepFilter
        last_modified() -> KeepFilter
```

## Others

-   Filesystem level deduplication
    -   http://dashohoxha.fs.al/deduplicating-data-with-xfs-and-reflinks/
