from typing import List, Optional, Type

from recompose.cursor import Cursor
from recompose.exceptions import NoCursorForCondition, UnsupportedVersion
from recompose.options import Options
from recompose.types import CursorSchema

_types: List[Type[Cursor]] = []


def make_cursor(
    schema: CursorSchema,
    options: Optional[Options] = None,
    require_version: bool = True,
) -> Cursor:
    """
    Creates and returns a cursor to handle a given transformer.
    """

    if require_version:
        if "version" not in schema:
            raise UnsupportedVersion.no_version(schema)

        if not isinstance(schema["version"], int):
            raise UnsupportedVersion.not_integer(schema["version"])

        if schema["version"] < 1 or schema["version"] > 1:
            raise UnsupportedVersion.unsupported(schema["version"], 1)

    condition = schema.get("on", "this-value")

    for t in _types:
        if condition == t.condition():
            return t(
                schema,
                options=options,
            )

    raise NoCursorForCondition(condition)


def register_cursor(cursor: Type[Cursor]) -> None:
    """
    Registers a cursor type.
    """

    _types.append(cursor)
