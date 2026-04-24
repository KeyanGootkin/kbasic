"""
    Use ABCs to allow matching any number or array type, e.g. this will work:
    match 1.:
        case Number(): ...
    
    or:
    match {1, 2, 3, 4}:
        case Array(): ...
"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from abc import ABC
from collections.abc import Generator
from numpy import int8, uint8, int16, uint16, int32, uint32, int64, uint64, \
                  float16, float32, float64, longdouble, complex64, complex128, \
                  clongdouble, ndarray
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class Array(ABC):
    types: list = [ndarray, list, set, tuple, Generator]
    @classmethod
    def __subclasshook__(cls, sub):
        return sub in cls.types
class Number(ABC):
    types: list = [
        int, int8, uint8, int16, uint16, int32, uint32, int64, uint64,
        float, float16, float32, float64, longdouble,
        complex, complex64, complex128, clongdouble
    ]
    @classmethod
    def __subclasshook__(cls, sub):
        return sub in cls.types
