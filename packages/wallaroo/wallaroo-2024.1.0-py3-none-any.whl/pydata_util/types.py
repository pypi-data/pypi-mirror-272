"""This module defines custom data types."""

from enum import Enum
from typing import TypeVar

SupportedFrameworks = TypeVar("SupportedFrameworks")


class ArrowListDType(str, Enum):
    """This class defines the possible PyArrow list data types."""

    LIST = "list"
    FIXED_SHAPE_TENSOR = "fixed-shape-tensor"


class IOArrowDType(str, Enum):
    """This class defines the possible Arrow pa.ChunkedArray
    data types for the input and output to/from
    an ArrowFlightServer."""

    LIST = ArrowListDType.LIST.value
    FIXED_SHAPE_TENSOR = ArrowListDType.FIXED_SHAPE_TENSOR.value
    SCALAR = "scalar"


class SupportedNATSMessages(str, Enum):
    """This class defines the supported NATS message types."""

    CONVERSION = "conversion"
    PACKAGING = "packaging"
