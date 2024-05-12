from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional

from recompose.logging import log
from recompose.options import Options
from recompose.transformer import Transformer
from recompose.transformers import find_transformer
from recompose.types import AnyTransformSchema, CursorSchema


class Cursor(ABC):
    """
    Cursor.
    """

    def __init__(
        self,
        schema: CursorSchema,
        options: Optional[Options] = None,
    ) -> None:
        self._schema = schema
        self.options = options

    def _make_transformer(
        self,
        schema: AnyTransformSchema,
    ) -> Transformer:
        return find_transformer(
            schema,
            options=self.options,
        )

    def __str__(self) -> str:
        return self.condition()

    @abstractmethod
    def _transform(self, data: Any) -> Any:
        """
        Transforms and returns the data.
        """

    @classmethod
    @abstractmethod
    def condition(cls) -> str:
        """
        Key.
        """

    def transform(self, data: Any) -> Any:
        """
        Transforms and returns the data.
        """

        log.debug("%s started transforming %s", self, data)
        return self._transform(data)

    @property
    def transformers(self) -> Iterable[Transformer]:
        """
        Yields each transformer.
        """

        if isinstance(self._schema["perform"], list):
            for transform in self._schema["perform"]:
                yield self._make_transformer(
                    transform,
                )

        else:
            yield self._make_transformer(
                self._schema["perform"],
            )
