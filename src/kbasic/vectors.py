# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from numpy import array, ndarray, cos, arccos, sin, arcsin, sqrt, float64, float32, exp, pi, complex128
from typing import Self
from collections.abc import Generator
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class Number:
    types: list = [float, float64, float32, int, complex, complex128]
class Iterable:
    types: list = [list, ndarray, tuple, Generator]
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def hamilton_product(q1, q2):
    a1, b1, c1, d1 = q1 
    a2, b2, c2, d2 = q2
    return array([
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2
    ], dtype=float)
def organize_components(components) -> tuple[float|int]:
    match components:
        case (x, *_) if type(x) in Number.types: return components
        case (x,) if type(x) in Iterable.types: return tuple(x) 
        case (Generator(),): return tuple(components[0])
        case (Vector(),): return components[0].components
        case _: raise TypeError(f"{components} cannot be matched")
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class Vector:
    def __init__(self, *components) -> None:
        self.components = organize_components(components)
        self.ndims = self.dim = self.dimensions = len(components) #i always forget which one i choose :)
    def __repr__(self) -> str: 
        return str(self.components)
    def __len__(self) -> int: 
        return self.dimensions
    def __abs__(self) -> Number: 
        return sqrt(sum(array(self.components)**2))
    def __iter__(self) -> Self:
        self._index = 0
        return self 
    def __next__(self) -> Number:
        try:
            value = self.components[self._index]
            self._index += 1
            return value
        except IndexError: raise StopIteration
    def __add__(self, other) -> Self:
        match other:
            case Vector(): return type(self)(xs+xo for xs, xo in zip(self.components, other.components))
            case x if type(x) in Number.types: return type(self)(x+other for x in self.components)
            case x if type(x) in Iterable.types: return type(self)(xs+xo for xs, xo in zip(self.components, other))
    def __sub__(self, other) -> Self:
        match other:
            case x if type(x) in Number.types: return type(self)(x-other for x in self.components)
            case x if type(x) in Iterable.types: return type(self)(xs-xo for xs, xo in zip(self.components, other))
            case Vector(): return type(self)(xs-xo for xs, xo in zip(self.components, other.components))
    def __mul__(self, other) -> Self|Number:
        match other:
            case Vector(): return sum([c1*c2 for c1,c2 in zip(self.components, other.components)])
            case x if type(x) in Number.types: return type(self)(c*other for c in self.components)            
    def __truediv__(self, other) -> Self:
        match other:
            case x if type(x) in Number.types: return type(self)(c/other for c in self.components)
    def __floordiv__(self, other) -> Self:
        match other:
            case x if type(x) in Number.types: return type(self)(c//other for c in self.components)
    def __radd__(self, other) -> Self: 
        match other:
            case 0: return self
            case _: return self.__add__(other)
    def __rsub__(self, other) -> Self: 
        match other:
            case 0: return self
            case _: return self.__sub__(other)
    def __rmul__(self, other) -> Self|Number: 
        match other:
            case 0: return self
            case _: return self.__mul__(other)
    def __rtruediv__(self, other) -> Self: 
        match other:
            case 0: return self
            case _: return self.__truediv__(other)
    def __rfloordiv__(self, other) -> Self: 
        match other:
            case 0: return self
            case _: return self.__floordiv__(other)

class Norm(Vector):
    def __init__(self, *components):
        components: tuple = organize_components(components)
        Vector.__init__(self, *components)
        gen = (x/abs(self) for x in self.components)
        Vector.__init__(self, gen)
class Quaternion(Norm):
    def __init__(self, angle, axis):
        q0 = cos(angle/2)
        self.axis = sin(angle/2)*Vector(axis)
        self.axis *= sqrt(1-q0**2)/abs(self.axis)
        Norm.__init__(self, q0, *self.axis.components)
        
class R2(Vector):
    def __init__(self, *components):
        self.components: tuple[Number] = organize_components(components)
        self.x, self.y = self.components
        Vector.__init__(self, *components)
        self.magnitude = abs(self)
        self.direction = Norm(*self.components) if self.magnitude>0 else None 
    def rotate(self, angle):
        r = self.x + 1j*self.y 
        r_rotated = r * exp(1j*angle)    
        self.__init__(r_rotated.real, r_rotated.imag)    
class R3(Vector):
    def __init__(self, *components):
        self.components: tuple[Number] = organize_components(components)
        self.x, self.y, self.z = self.components
        Vector.__init__(self, *self.components)
        self.magnitude = abs(self)
        self.direction = Norm(*self.components) if self.magnitude>0 else None
    def from_spherical(radius: Number, azimuth: Number, latitude: Number) -> Self:
        x = radius * cos(azimuth) * sin(latitude)
        y = radius * sin(azimuth) * sin(latitude)
        z = radius * cos(latitude)
        return R3(x, y, z)
    def rotate(self, angle, axis):
        axis = array(axis)
        qs = array([0, *self.components])
        rotation = array(Norm([cos(angle/2), *(axis*sin(angle/2))]).components)
        rotation_inverse = array([rotation[0], *-rotation[1:]])
        rotated_vector = hamilton_product(hamilton_product(rotation, qs), rotation_inverse)[1:]
        self.__init__(*rotated_vector)

class Matrix:
    def __init__(self, array):
        self.array = array 
    def __mul__(self, other):
        match other:
            case Vector():
                res = [[self.array[i,j]*other.components[i] for i in range(len(other))] for j in range(len(other))]