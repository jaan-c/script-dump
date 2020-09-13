from typing import *
import os, json
from . import logic


class _PrimitiveFileTag(TypedDict):
    path: str
    tags: List[str]


def save_file_tags(
    file_tags: Sequence[logic.FileTag], path: str = _get_data_path()
) -> None:
    parent_dir = os.path.dirname(path)
    os.makedirs(parent_dir, exist_ok=True)

    with open(path, "w") as file:
        json.dump([_as_primitive(ft) for ft in file_tags], file)


def read_file_tags(path: str = _get_data_path()) -> List[logic.FileTag]:
    with open(path, "r") as file:
        primitive_file_tags = json.load(file)

    return [_from_primitive(pft) for pft in primitive_file_tags]


def _get_data_path() -> str:
    home = os.getenv("HOME")
    file_name = "ftags.json"

    if home is None:
        raise EnvironmentError("undefined $HOME environment variable")

    return os.path.join(home, ".local", "share", file_name)


def _as_primitive(file_tag: logic.FileTag) -> _PrimitiveFileTag:
    return {"path": file_tag.path, "tags": list(file_tag.tags)}


def _from_primitive(primitive: _PrimitiveFileTag) -> logic.FileTag:
    return logic.FileTag(path=primitive["path"], tags=primitive["tags"])
