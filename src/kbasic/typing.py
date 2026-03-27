"""
    I don't like type checking in python, so the way i decided to do it is if i want
    to see if something looks like a number (int, float, complex or numpy variants)
    i would say ->
    if type(x) in Number.types: do_something()
    elif type(x) in Array.types: do_something_else()
"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from numpy import int8, uint8, int16, uint16, int32, uint32, int64, uint64, \
                  float16, float32, float64, longdouble, complex64, complex128, \
                  clongdouble, ndarray
from numpy.typing import NDArray, ArrayLike
from collections.abc import Callable, Generator
from typing import Any
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class Array:
    types: list = [NDArray, ndarray, list, set, tuple, Generator]
class Number:
    types: list = [
        int, int8, uint8, int16, uint16, int32, uint32, int64, uint64, 
        float, float16, float32, float64, longdouble, 
        complex, complex64, complex128, clongdouble
    ]
    def __new__(cls, x):
        match x:
            case x if type(x) in Number.types: return x
            case str() if x.isnumeric(): return int(x)
            case str() if '.' in x and all([xi.isnumeric() for xi in x.split('.')]): 
                return float(x)
            case _: raise ValueError(f"Cannot parse argument: {x}\nof type: {type(x)}")
