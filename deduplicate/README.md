# deduplicate

```
usage: main.py [-h] [--keep-most-recent] dir_path

recursively deduplicate files in dir_path

positional arguments:
  dir_path            directory to deduplicate

optional arguments:
  -h, --help          show this help message and exit
  --keep-most-recent  automatically keep most recent file and delete other
                      duplicates

If --keep-most-recent is supplied, deduplication happens automatically,
otherwise an interactive interface is shown.
```
