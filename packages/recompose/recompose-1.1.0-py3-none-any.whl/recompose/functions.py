from typing import Any, Optional

from recompose.cursors import make_cursor
from recompose.options import Options
from recompose.types import CursorSchema


def transform(
    schema: CursorSchema,
    data: Any,
    options: Optional[Options] = None,
) -> Any:
    """
    Transforms and returns `data` according to `schema`.

    `options` describes the transformation's run-time options. Sensible defaults
    will be used by default.
    """

    cursor = make_cursor(
        schema,
        options=options,
    )

    return cursor.transform(data)
