"""This module defines custom exceptions for the pydata-utils package."""


import functools
import logging
from pathlib import Path
from typing import Any, Set, Type

logger = logging.getLogger(__name__)


class DirectoryNotExistError(Exception):
    """This exception is raised if the directory does not exist."""

    def __init__(self, message: str) -> None:
        """Initializes the DirectoryNotExistError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class FileFormatError(Exception):
    """This exception is raised if the file format of the given file path
    is not supported."""

    def __init__(self, message: str) -> None:
        """Initializes the FileFormatError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class PathNotExistError(Exception):
    """This exception is raised if the path does not exist."""

    def __init__(self, message: str) -> None:
        """Initializes the PathNotExistError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class SubclassTypeNotExistError(Exception):
    """This exception is raised if the subclass type does not exist
    whenever an AbstractFactory is used."""

    def __init__(self, message: str) -> None:
        """Initializes the SubclassTypeNotExistError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


def log_error(exception_type: Type[Exception], message: str) -> Any:
    """This helper function logs the error and raises the given exception type.

    :param exception_type: The type of the exception to raise.
    :param message: The message to log.

    :raises exception_type: The given exception type.

    :return: The wrapped function.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                logger.error(message, exc_info=True)
                raise exception_type(message) from exc

        return wrapper

    return decorator


def raise_directory_not_exists_if_no_dir(
    directory: Path,
) -> None:
    """Raise an error if the directory doesn't exist.

    :param directory: Path to the directory.

    :raises DirectoryNotExistError: If there is no directory at the given path, then
        DirectoryNotExistError is raised.
    """
    if not directory.is_dir():
        message = f"There is no directory at: '{directory.as_posix()}'."
        logger.error(message)
        raise DirectoryNotExistError(message)


def raise_file_format_error_if_file_format_incorrect(
    file_path: Path, supported_file_formats: Set[str]
) -> None:
    """Raise a FileFormatError if the format of the given file is not supported, i.e.,
    the format of the given file is not in the supported_file_formats.

    :param file_path: The path of the file which we want to check the validity
        of its format. The file must exist.
    :param supported_file_formats: A list of supported file formats.
        The concrete classes that deal with files should define this attribute.

    :raises FileFormatError: If the format of the given file is not in the
        supported_file_formats list, then a FileFormatError is raised.
    """
    file_format = file_path.suffix[1:]
    if file_format not in supported_file_formats:
        message = (
            f"File format {file_format} is not supported. "
            f"Supported file formats are: {supported_file_formats}."
        )
        logger.error(message)
        raise FileFormatError(message)


def raise_path_not_exist_error_if_no_path(
    path: Path,
) -> None:
    """This helper function raises an error if the path passed doesn't exist.

    :param path: Path of a file.

    :raises PathDoesNotExistError: If there is no file at the given path, then
        PathDoesNotExistError is raised.
    """
    if not path.exists():
        message = f"There is no file or directory at: '{path.as_posix()}'."
        logger.error(message)
        raise PathNotExistError(message)
