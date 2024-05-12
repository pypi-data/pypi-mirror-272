from typing import Any


class PathNotFound(IndexError):
    """
    Raised when a path cannot be found in a record.
    """

    def __init__(
        self,
        path: str,
        record: Any,
    ) -> None:
        super().__init__(f'Path "{path}" not found in record {record}')
