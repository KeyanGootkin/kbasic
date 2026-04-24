"""Implement vector classes for vector analysis"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                                    Imports                                     <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from typing import Self
from collections.abc import Generator
from functools import total_ordering
from numpy import array, cos, sin, sqrt, exp, sum
from kbasic.typing import Number, Array

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                                   Functions                                    <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def hamilton_product(q1, q2):
    """the hamilton product between two quaternions"""
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return array([
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2
    ], dtype=float)

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                                    Classes                                     <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class VectorBase:
    def __init__(self, *components) -> None:
        match components[0]:
            case Number():
                self.components = components
            case Array():
                self.components = tuple(array(x) for x in components)
            case Generator():
                self.components = tuple(components[0])
            case x: raise TypeError(f"given components of type: {type(x)}")
        #i always forget which one i choose :)
        self.ndims = self.dim = self.dimensions = len(components)
    def __repr__(self) -> str:
        return f"Vector{str(self.components)}"
    def __len__(self) -> int:
        return len(self.components[0]) if type(self.components[0]) in Array.types else 1
    def __abs__(self) -> Number:
        return sqrt(sum(array(self.components)**2, axis=0))
    def __eq__(self, other) -> bool:
        match other:
            case VectorBase():
                if len(self) > 1 or len(other) > 1:
                    return all(all(s==o) for s,o in zip(self, other))
                return all(s==o for s, o in zip(self, other))
            case x if type(x) in Array.types:
                return all(all(s==o) for s, o in zip(self, other))
            case _:
                return False
    def __getitem__(self, item):
        match item:
            case int():
                return Vector(c[item] for c in self.components)
            case (int(), *_):
                return Vector([c[i] for i in item] for c in self.components)
            case slice():
                start = item.start if item.start else 0
                stop = item.stop if item.stop else len(self)
                step = item.step if item.step else 1
                return Vector([c[i] for i in range(start, stop, step)] for c in self.components)
    def __iter__(self) -> Self:
        self._index = 0
        return self
    def __next__(self) -> Number:
        try:
            value = self.components[self._index]
            self._index += 1
            return value
        except IndexError as err: raise StopIteration from err
    def __add__(self, other) -> Self:
        match other:
            case VectorBase():
                return Vector(xs+xo for xs, xo in zip(self.components, other.components))
            case Number():
                return Vector(xi+other for xi in self)
            case Array():
                return Vector(xs+xo for xs, xo in zip(self.components, other))
    def __sub__(self, other) -> Self:
        match other:
            case Number():
                return type(self)(x-other for x in self)
            case Array():
                return type(self)(xs-xo for xs, xo in zip(self.components, other))
            case VectorBase():
                return type(self)(xs-xo for xs, xo in zip(self.components, other.components))
    def __mul__(self, other) -> Self|Number:
        match other:
            case VectorBase():
                return sum(list(c1*c2 for c1,c2 in zip(self, other)), axis=0)
            case Number():
                return type(self)(c*other for c in self)
            case Array():
                return type(self)(c1*c2 for c1, c2 in zip(self, other))
    def __truediv__(self, other) -> Self:
        match other:
            case VectorBase():
                return Vector(c1 / c2 for c1, c2 in zip(self, other))
            case Number():
                return type(self)(c / other for c in self)
            case Array():
                return type(self)(c1 / c2 for c1, c2 in zip(self, other))
    def __floordiv__(self, other) -> Self:
        match other:
            case Number():
                return type(self)(c//other for c in self)
            case Array():
                return type(self)(c1//c2 for c1, c2 in zip(self, other))
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
            case Number():
                return type(self)(other/c for c in self)
            case Array():
                return type(self)(c2/c1 for c1, c2 in zip(self, other))
    def __rfloordiv__(self, other) -> Self:
        match other:
            case Number():
                return type(self)(other//c for c in self)
            case Array():
                return type(self)(c2//c1 for c1, c2 in zip(self, other))
class Vector(VectorBase):
    def __new__(cls, *components) -> Self: # the vector factory
        match components:
            # vector
            case (VectorBase(),):
                return components[0]
            # generator
            case (Generator(),):
                return Vector(tuple(components[0]))
            # single array
            case (Array(),):
                return Vector(*x)
            # 2D
            case (x, y):
                return R2(x, y)
            # 3D
            case (x, y, z):
                return R3(x, y, z)
            # several numbers
            case x if all(type(xi) in Number.types for xi in x):
                return VectorBase(*components)
            # several arrays
            case x if all(type(xi) in Array.types for xi in x):
                return VectorBase(*components)
            case x:
                raise TypeError(f"given components:\n{components}\nof type: {type(x)}")
class Norm(VectorBase):
    def __init__(self, *components):
        self.components = components
        gen = (x/abs(self) for x in self)
        super().__init__(gen)
class Quaternion(Norm):
    def __init__(self, angle, axis):
        q0 = cos(angle/2)
        self.axis = Vector(*axis)
        self.axis *= sin(angle/2)
        self.axis *= sqrt(1-q0**2)/abs(self.axis)
        super().__init__(q0, *self.axis.components)
class R2(VectorBase):
    def __init__(self, *components):
        super().__init__(*components)
        self.x, self.y = self.components
        self.magnitude = abs(self)
        # self.direction = Norm(*self.components) if self.magnitude>0 else None
    def rotate(self, angle) -> Self:
        """docstring"""
        r = self.x + 1j*self.y
        r_rotated = r * exp(1j*angle)
        self.__init__(r_rotated.real, r_rotated.imag)
        return self
class R3(VectorBase):
    def __init__(self, *components):
        super().__init__(*components)
        self.x, self.y, self.z = self.components
        self.magnitude = abs(self)
        # self.direction = Norm(*self.components) if self.magnitude>0 else None
    def from_spherical(radius: Number, azimuth: Number, latitude: Number) -> Self:
        """docstring"""
        x = radius * cos(azimuth) * sin(latitude)
        y = radius * sin(azimuth) * sin(latitude)
        z = radius * cos(latitude)
        return R3(x, y, z)
    def rotate(self, angle, axis):
        """docstring"""
        axis = array(axis)
        qs = array([0, *self.components])
        rotation = array(Norm(cos(angle/2), *(axis*sin(angle/2))).components)
        rotation_inverse = array([rotation[0], *-rotation[1:]])
        rotated_vector = hamilton_product(hamilton_product(rotation, qs), rotation_inverse)[1:]
        self = R3(*rotated_vector)
        return self
    def cross(self, other: Self) -> Self:
        """Compute self cross other"""
        x = self.y*other.z - self.z*other.y
        y = -(self.x*other.z - self.z*other.x)
        z = self.x*other.y - self.y-other.z
        return R3(x, y, z)
