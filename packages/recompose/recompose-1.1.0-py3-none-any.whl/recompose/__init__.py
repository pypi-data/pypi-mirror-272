"""
Recompose is a Python package for templated data recomposition.
"""

from importlib.resources import files

import recompose.cursor_classes
import recompose.transformer_classes
from recompose.cursors import make_cursor, register_cursor
from recompose.enums import Allow
from recompose.exceptions import (
    InvalidSchema,
    NoCursorForCondition,
    NotATransformerType,
    PathNotFound,
    RecomposeError,
    UnsupportedVersion,
)
from recompose.functions import transform
from recompose.options import Options
from recompose.transformer import Transformer
from recompose.transformers import find_transformer, register_transformer
from recompose.types import CursorSchema

with files(__package__).joinpath("VERSION").open("r") as t:
    __version__ = t.readline().strip()


register_cursor(recompose.cursor_classes.EachValue)
register_cursor(recompose.cursor_classes.ThisValue)

register_transformer(recompose.transformer_classes.ListToObject)
register_transformer(recompose.transformer_classes.Pass)


__all__ = [
    "Allow",
    "CursorSchema",
    "InvalidSchema",
    "NoCursorForCondition",
    "NotATransformerType",
    "Options",
    "PathNotFound",
    "RecomposeError",
    "Transformer",
    "UnsupportedVersion",
    "make_cursor",
    "find_transformer",
    "transform",
]
