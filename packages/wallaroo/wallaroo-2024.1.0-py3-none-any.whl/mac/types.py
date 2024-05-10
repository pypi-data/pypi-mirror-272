"""This module defines custom types for the mac package."""

from enum import Enum
from typing import Callable, Dict, Tuple, Union

import numpy.typing as npt
import pyarrow as pa
from typing_extensions import TypeAlias

# PythonStep related types
InferenceData: TypeAlias = Dict[str, npt.NDArray]
PythonStep: TypeAlias = Callable[[InferenceData], InferenceData]

# Arrow converters
ArrowToNDArrayConverter: TypeAlias = Callable[[pa.ChunkedArray], npt.NDArray]
NDArrayToArrowConverter: TypeAlias = Callable[
    [npt.NDArray],
    Tuple[pa.DataType, Union[pa.Array, pa.ListArray, pa.ExtensionArray]],
]


class SupportedFrameworks(str, Enum):
    """This class defines an Enum for supported frameworks. The frameworks are used
    to load a `PythonStep`.
    """

    KERAS = "keras"
    SKLEARN = "sklearn"
    PYTORCH = "pytorch"
    XGBOOST = "xgboost"
    HUGGING_FACE = "hugging-face"
    CUSTOM = "custom"  # BYOP
    PYTHON = "python"  # pre/post-processing step


class SupportedServices(str, Enum):
    """This class defines an Enum for supported services that
    can be used to serve a `PythonStep` for inference purposes.
    """

    MLFLOW = "mlflow"
    FLIGHT = "flight"
