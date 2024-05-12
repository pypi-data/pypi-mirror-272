from typing import Any

from recompose.cursors import make_cursor
from recompose.enums import ALLOWS, Allow
from recompose.exceptions import PathNotFound
from recompose.logging import log
from recompose.options import Options
from recompose.schema_readers import CursorSchemaReader, PathReader
from recompose.transformer import Transformer


class Pass(Transformer):
    """
    Passes transformation to child data.
    """

    def _transform(self, data: Any) -> Any:
        cursor_schema = CursorSchemaReader.get_required(self.schema)

        cursor = make_cursor(
            cursor_schema,
            options=self.options,
            require_version=False,
        )

        path = PathReader.get_required(self.schema)

        try:
            child_data = data[path]

        except KeyError:
            options = self.options or Options()

            if options.missing_data in ALLOWS:
                if options.missing_data == Allow.ALLOW_WITH_WARNING:
                    log.warning(
                        'Path "%s" not found in record %s',
                        path,
                        data,
                    )

                return data

            raise PathNotFound(
                path,
                data,
            )

        log.debug('%s will transform %s from path "%s"', self, child_data, path)
        transformed = cursor.transform(child_data)

        return {
            **data,
            path: transformed,
        }

    @classmethod
    def name(cls) -> str:
        return "pass"
