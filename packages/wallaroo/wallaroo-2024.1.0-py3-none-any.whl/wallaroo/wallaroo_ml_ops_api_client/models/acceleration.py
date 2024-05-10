from enum import Enum


class Acceleration(str, Enum):
    AIO = "aio"
    CUDA = "cuda"
    JETSON = "jetson"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
