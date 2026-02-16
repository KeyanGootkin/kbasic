from numpy import ndarray, int8, uint8, int16, uint16, int32, uint32, int64, uint64, float16, float32, float64, longdouble, complex64, complex128, clongdouble

class Number:
    types: list = [
        int, int8, uint8, int16, uint16, int32, uint32, int64, uint64, 
        float, float16, float32, float64, longdouble, 
        complex, complex64, complex128, clongdouble
    ]

class Iterable:
    types: list = [
        list, set, dict, tuple, ndarray
    ]