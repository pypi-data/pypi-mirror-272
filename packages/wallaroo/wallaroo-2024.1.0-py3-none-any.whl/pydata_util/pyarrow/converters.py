"""This module features converter functions for pyarrow."""

import logging
from typing import Tuple

import numpy as np
import numpy.typing as npt
import pyarrow as pa

from pydata_util.numpy.converters import convert_multi_dim_numpy_array_to_list
from pydata_util.pyarrow.data_inspectors import (
    get_arrow_list_dtype_from_pa_dtype,
    get_data_type_of_nested_list,
    get_max_depth_of_nested_list,
    get_pa_struct_dtype_from_dict_array,
    get_shape_of_multi_dim_chunked_array,
    pa_type_is_list,
)

logger = logging.getLogger(__name__)


def convert_fixed_shape_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts a fixed shape multi-dim pa.ChunkedArray to a numpy array.

    :param array: The pa.ChunkedArray object to convert.

    :return: The converted data to a multi-dim numpy array.
    """
    shape = get_shape_of_multi_dim_chunked_array(
        array=array,
        arrow_list_dtype=get_arrow_list_dtype_from_pa_dtype(array.type),
    )
    return np.array(
        [
            row
            for chunk in array.chunks
            for row in flat_values(chunk)
            .to_numpy(zero_copy_only=False)
            .reshape([len(chunk), *shape])
        ]
    )


def convert_irregular_shape_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts an irregular shape multi-dim pa.ChunkedArray to a numpy array.

    :param array: The pa.ChunkedArray to convert.

    :return: The converted data to a multi-dim numpy array of type `np.object`.
    """
    return np.array(
        [row for chunk in array.chunks for row in chunk.to_numpy(zero_copy_only=False)],
        dtype=object,
    )


def convert_multi_dim_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts a PyArrow chunked array to a numpy array.

    :param array: The PyArrow ChunkedArray to convert.

    :return: The converted data to a numpy array.
    """

    try:
        return convert_fixed_shape_chunked_array_to_numpy_array(array)
    except (ValueError, IndexError):
        # The incoming array is not of fixed shape, so we need to
        # return a numpy array of type object.
        return convert_irregular_shape_chunked_array_to_numpy_array(array)


def convert_numpy_array_to_fixed_shape_tensor_array(
    data: npt.NDArray,
) -> Tuple[pa.FixedShapeTensorType, pa.ExtensionArray]:
    """Converts a numpy array to a fixed shape tensor array.

    :param data: The data to convert.

    :return: The converted data to a FixedShapeTensor array,
        along with the PyArrow data type.
    """
    data_type = pa.from_numpy_dtype(data.dtype)
    data_shape = data[0].shape
    tensor_type = pa.fixed_shape_tensor(
        data_type,
        data_shape,
    )
    flattened_array = [item.flatten().tolist() for item in data]

    storage = pa.array(
        flattened_array,
        pa.list_(data_type, len(flattened_array[0])),
    )
    tensor_array = pa.ExtensionArray.from_storage(tensor_type, storage)

    return (tensor_type, tensor_array)


def convert_numpy_array_to_nested_list_array(
    data: npt.NDArray,
) -> Tuple[pa.ListType, pa.ListArray]:
    """Converts a numpy array to a nested list array.

    :param data: The data to convert.

    :return: The converted data to a nested list array,
        along with the PyArrow data type.
    """
    try:
        data_type = pa.from_numpy_dtype(data.dtype)
    except pa.ArrowNotImplementedError:
        # it's a list of iterables (e.g. list, tuple, dict etc.)
        item_dtype = get_data_type_of_nested_list(data)

        try:
            data_type = (
                pa.null()
                if item_dtype == type(None)
                else (
                    get_pa_struct_dtype_from_dict_array(data)
                    if item_dtype == dict
                    else pa.from_numpy_dtype(item_dtype)
                )
            )
        except pa.ArrowNotImplementedError as exc:
            message = (
                f"Data type `{item_dtype}` of nested list cannot be converted to arrow.\n"  # noqa: E501
                f"Nested list that is causing this error: `{data}`."
            )
            logger.debug(message, exc_info=True)
            raise exc

    max_dim = get_max_depth_of_nested_list(data)
    nested_array = pa.array(
        convert_multi_dim_numpy_array_to_list(data),
        type=nested_pa_list_type_constructor(max_dim=max_dim, data_type=data_type),
    )

    return (nested_array.type, nested_array)


def convert_numpy_array_to_pa_array(
    data: npt.NDArray,
) -> Tuple[pa.ListType, pa.Array]:
    """Converts a numpy array to a pa.Array.

    :param data: The data to convert.

    :return: The converted data to a pa.Array,
        along with the PyArrow data type.
    """
    return pa.from_numpy_dtype(data.dtype), pa.array(data)


def flat_values(array: pa.ChunkedArray) -> pa.Array:
    """
    Recursively unnest the `array` until a non-list type is found.

    :param array: The PyArrow ChunkedArray to flatten.

    :return: The inner non-nested values array.
    """
    if isinstance(array, pa.FixedShapeTensorArray):
        array = array.storage
    while pa_type_is_list(array.type):
        array = array.values
    return array


def nested_pa_list_type_constructor(
    max_dim: int, data_type: pa.DataType
) -> pa.ListType:
    """This helper function constructs a nested PyArrow list type.

    :param max_dim: The number of dimensions of the nested list.
    :param data_type: The data type of the nested list.

    :return: The nested PyArrow ListType object.
    """
    while max_dim > 1:
        max_dim -= 1
        return pa.list_(nested_pa_list_type_constructor(max_dim, data_type))
    return data_type
