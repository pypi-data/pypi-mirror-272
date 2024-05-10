"""This modules contains data inspection functions for pyarrow."""

from typing import List, Tuple, Type, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa

from pydata_util.types import ArrowListDType, IOArrowDType


def get_arrow_list_dtype_from_pa_dtype(
    pa_type: pa.DataType,
) -> ArrowListDType:
    """Gets the ArrowListDType from a given pa.DataType.

    :param pa_type: The pa.DataType to convert.

    :return: The ArrowListDType.
    """
    if pa_type_is_fixed_shape_tensor(pa_type):
        return ArrowListDType.FIXED_SHAPE_TENSOR
    return ArrowListDType.LIST


def get_data_type_from_value_type(value_type: pa.DataType) -> pa.DataType:
    """Gets the data type from the given value type.

    :param value_type: The value type to get the data type from.

    :return: The PyArrow data type.
    """
    try:
        return get_data_type_from_value_type(value_type.value_type)
    except AttributeError:
        return value_type


def get_data_type_of_nested_list(data: Union[npt.NDArray, List]) -> Type:
    """Gets the data type of a nested list.
    :param data: The nested list to get the data type of.
    :return: The data type of the nested list.
    """
    if isinstance(data, (np.ndarray, list, tuple)):
        return get_data_type_of_nested_list(data[0])
    return type(data)


def get_arrow_type_of_nested_arrow_list_type(
    arrow_type: Union[pa.ListType, pa.FixedSizeListType],
) -> int:
    """Gets the PyArrow type of a nested PyArrow list.

    :param arrow_type: The nested list to get the type of.

    :return: The dtype id of the nested list.
    """
    if isinstance(arrow_type, (pa.ListType, pa.FixedSizeListType)):
        return get_arrow_type_of_nested_arrow_list_type(arrow_type.value_type)
    return arrow_type.id


def get_io_arrow_dtype_from_column(
    column_type: pa.DataType,
) -> IOArrowDType:
    """Gets the IOArrowDType from the given column.

    :param column: The column to get the IOArrowDType from.
    """
    if pa_type_is_fixed_shape_tensor(column_type):
        return IOArrowDType.FIXED_SHAPE_TENSOR
    elif pa_type_is_list(column_type):
        return IOArrowDType.LIST
    else:
        return IOArrowDType.SCALAR


def get_max_depth_of_nested_list(data: Union[npt.NDArray, List]) -> int:
    """Gets the maximum depth of a nested list.

    :param data: The nested list to get the maximum depth of.

    :return: The maximum depth of the nested list.
    """
    if isinstance(data, (np.ndarray, list)):
        depths = [get_max_depth_of_nested_list(element) for element in data]
        return 1 + max(depths)
    return 0


def get_pa_struct_dtype_from_dict_array(data: npt.NDArray) -> pa.DataType:
    """Gets the PyArrow data type from a numpy array of dictionaries.
    :param data: The data to get the PyArrow data type from.
    :return: The PyArrow data type.
    """
    while not isinstance(data, dict):
        data = data[0]

    struct_fields = []
    for key, value in data.items():
        try:
            struct_fields.append((key, pa.from_numpy_dtype(type(value))))
        except pa.ArrowNotImplementedError:
            # dict values are of type iterable
            item_dtype = get_data_type_of_nested_list(value)
            list_constructor = nested_pa_list_type_constructor(
                max_dim=len(value),
                data_type=pa.from_numpy_dtype(item_dtype),
            )
            struct_fields.append(
                (
                    key,
                    list_constructor,
                )
            )

    return pa.struct(struct_fields)


def get_shape_of_multi_dim_chunked_array(
    array: pa.ChunkedArray, arrow_list_dtype: ArrowListDType
) -> Tuple[int, ...]:
    """Gets the shape of a multi-dimensional pa.ChunkedArray.

    :param array: The multi-dimensional array to get the shape of.
    :param arrow_list_dtype: The ArrowListDType of the array.

    :return: The shape of the multi-dimensional pa.ChunkedArray.
    """
    if arrow_list_dtype == ArrowListDType.FIXED_SHAPE_TENSOR:
        return tuple(array.type.shape)
    # can only infer shape from first row
    return get_shape_of_nested_pa_list_scalar(array[0])


def get_shape_of_nested_arrow_list_type(
    arrow_type: pa.FixedSizeListType,
) -> Tuple[int, ...]:
    """Gets the shape of a nested pa.FixedSizeListType.

    :param data: The nested list to get the shape of.

    :return: The shape of the nested list.
    """
    if isinstance(arrow_type, pa.FixedSizeListType):
        return (arrow_type.list_size,) + get_shape_of_nested_arrow_list_type(
            arrow_type.value_type
        )
    return ()


def get_shape_of_nested_pa_list_scalar(
    data: pa.ListScalar,
) -> Tuple[int, ...]:
    """Gets the shape of a nested pa.ChunkedArray.

    :param data: The nested list to get the shape of.

    :return: The shape of the nested pa.ChunkedArray.
    """
    if isinstance(data, pa.ListScalar):
        if data.is_valid:
            return (len(data),) + get_shape_of_nested_pa_list_scalar(data[0])
        return (0,)
    return ()


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


def pa_type_is_fixed_shape_tensor(data_type: pa.DataType) -> bool:
    """Checks if the given PyArrow data type is a fixed shape tensor type.

    :param data_type: The data type to check.

    :return: True if the given data type is a fixed shape tensor type, False otherwise.
    """
    return isinstance(data_type, pa.FixedShapeTensorType)


def pa_type_is_list(data_type: pa.DataType) -> bool:
    """Checks if the given PyArrow data type is a list type.

    :param data_type: The data type to check.

    :return: True if the given data type is a list type, False otherwise.
    """
    return isinstance(data_type, (pa.ListType, pa.FixedSizeListType))
