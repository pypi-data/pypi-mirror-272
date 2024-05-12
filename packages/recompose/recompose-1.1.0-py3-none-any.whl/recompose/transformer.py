from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from recompose.logging import log
from recompose.options import Options
from recompose.types import TransformSchema


class Transformer(ABC):
    """
    Abstract transformer.
    """

    def __init__(
        self,
        schema: TransformSchema,
        options: Optional[Options] = None,
    ) -> None:
        self._schema = schema
        self.options = options
        log.debug("Created %s with %s", self, schema)

    def __str__(self) -> str:
        return self.name()

    @abstractmethod
    def _transform(self, data: Any) -> Any:
        """
        Transforms and returns the data.
        """

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
        Key.
        """

    @property
    def schema(self) -> TransformSchema:
        """
        Schema.
        """

        return self._schema

    def transform(self, data: Any) -> Any:
        """
        Transforms and returns the data.
        """

        log.debug("%s started transforming %s", self, data)
        transformed = self._transform(data)
        log.debug("%s transformed %s to %s", self, data, transformed)
        return transformed
